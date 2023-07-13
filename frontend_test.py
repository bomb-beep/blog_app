from requests import get,post
import backend_test

def test(method,request,args = {}):
	# if request[-1] != "/":
	# 	request = request + "/"
	print(f"--{request}--")
	response = method("http://127.0.0.1:5000/"+request,json=args)
	print(f"Status code: {response.status_code}")
	print(f"Content-type: {response.headers['Content-type']}")
	if response.headers["Content-type"] == "application/json":
		print(f"{response.json()}\n")
	elif "text/html" in response.headers["Content-type"]:
		print(f"{response.text}\n")
	else:
		print(f"{response.content}\n")
	return response.status_code

def check(request,expected_response=None):
	# if request[-1] != "/":
	# 	request = request + "/"
	print(f"check {request}")
	response = get("http://127.0.0.1:5000/"+request)
	if expected_response is not None:
		print(f"Expected response: {expected_response},  actual response: {response}")
	if response.content is None:
		print(f"{response.status_code}")
	elif response.headers["Content-type"] == "application/json":
		print(f"Status code: {response.status_code}\n{response.json()}\n\n")
	else:
		print(f"Status code: {response.status_code}\n{response.content}\n\n")
	return response.status_code

# check("login")
# test(get,"login")
# test(post,"login")
print("\nFrontend Test\n")
print("Checking url")
url = "http://127.0.0.1:5000/"
response = get(url)
print("Status code:",response.status_code)
assert 200 == response.status_code
assert "Forste innlegg" in response.text

print("\nChecking post")
response = get(url+"1")
print("Status code:",response.status_code)
assert 200 == response.status_code
assert "Logg inn" in get(url).text

print("\nChecking create new post without login")
response = get(url+"create")
print("Status code:",response.status_code)
assert 401 == response.status_code

print("\nChecking login")
assert 200 == get(url+"login").status_code

print("\nChecking login - wrong username")
response = post(url+"login",data={"username":"sef","password":"passord123"})
assert "Incorrect username" in response.text
assert "session" not in response.cookies

print("\nChecking login - wrong password")
response = post(url+"login",data={"username":"sjef","password":"passord"})
assert "Incorrect password" in response.text
assert "session" not in response.cookies

print("\nChecking login - correct")
response = post(url+"login",data={"username":"sjef","password":"passord123"})
print("Status code:",response.status_code)
assert 200 == response.status_code
if response.history:
	assert "session" in response.history[0].cookies
	sjef_session = response.history[0].cookies
else:
	assert "session" in response.cookies
	sjef_session = response.cookies
assert "Logg inn" not in get(url,cookies=sjef_session).text

print("\nChecking create new post")
response = get(url+"create",cookies=sjef_session)
print("Status code:",response.status_code)
assert 200 == response.status_code
assert 404 == get(url+"2").status_code
post(url+"create",data={"title":"Andre innlegg","body":"mer innhold"},cookies=sjef_session)
assert 200 == get(url+"2").status_code

print("\nLogging in non-admin")
response = post(url+"login",data={"username":"bot","password":"passord123"})
if response.history:
	assert "session" in response.history[0].cookies
	bot_session = response.history[0].cookies
else:
	assert "session" in response.cookies
	bot_session = response.cookies

print("\nChecking create post as non-admin")
response = post(url+"create",data={"title":"Viktig!!!","body":"http://virus.no"},cookies=bot_session)
print("Status code:",response.status_code)
assert 403 == response.status_code
assert 404 == get(url+"3").status_code

print("\nAdding comment")
response = post(url+"2/comment",data={"body":"!!!"},cookies=bot_session)
print("Status code:",response.status_code)

print("\nTesting register user")
response = post(url+"register",data={"username":"bruker2","password":"passord123"})
if response.history:
	assert "session" in response.history[0].cookies
	bruker_session = response.history[0].cookies
else:
	assert "session" in response.cookies
	bruker_session = response.cookies
assert "bruker2" in get(url,cookies=bruker_session).text
response = post(url+"2/comment",data={"body":"kommentar"},cookies=bruker_session)
assert 200 == response.status_code
assert "fra bruker2" in get(url+"2").text
# form = {"username":"sjef","password":"passord123"}
# response = post(url+"login",data=form)
# print(response.status_code)
# session = response.cookies
# print(session)

# response = get(url+"",cookies=session)
# print(response.status_code,response.text)