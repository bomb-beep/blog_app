from flask import g,current_app
import click
import backend.db


@click.command("init-db")
def init_db_command():
	backend.db.init_db()
	click.echo("Initialized the database")

def close_db(e=None):
	if "db" in g:
		g["db"].close()

def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)

def get_db():
	if "db" not in g:
		g["db"] = backend.db.get_db()

	return g["db"]