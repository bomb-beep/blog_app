from requests import get,post
import backend_test

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
response = post(url+"register",data={"username":"mod","password":"passord123"})
if response.history:
	assert "session" in response.history[0].cookies
	mod_session = response.history[0].cookies
else:
	assert "session" in response.cookies
	mod_session = response.cookies
assert "mod" in get(url,cookies=mod_session).text
response = post(url+"2/comment",data={"body":"kommentar"},cookies=mod_session)
assert 200 == response.status_code
assert "fra mod" in get(url+"2").text

print("\nTesting set admin")
response = get(url+"administrator",cookies=mod_session)
assert 403 == response.status_code
response = get(url+"administrator",cookies=sjef_session)
assert 200 == response.status_code
response = post(url+"administrator",data={"username":"mod","admin":"1"},cookies=sjef_session)
post(url+"create",data={"title":"Ny moderator","body":"Hei allesammen!"},cookies=mod_session)
assert 200 == get(url+"3").status_code
response = post(url+"administrator",data={"username":"mod","admin":"0"},cookies=sjef_session)
post(url+"create",data={"title":"Moderator","body":"Forste dag paa job!"},cookies=mod_session)
assert 404 == get(url+"4").status_code

print("\n\n\n!!! Frontend tests complete !!!")