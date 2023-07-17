from .db import get_db
from datetime import date


def add_post(title,content,user):
    if user["er_admin"] == True:
        db = get_db()
        db.execute("INSERT INTO innlegg (tittel,innhold,bruker_id) VALUES "
                   "(?,?,?)",
                   (title,content,user["id"]))
        db.commit()
        
def get_post(id):
    post = get_db().execute(
        "SELECT i.id,tittel,innhold,dato_postet,brukernavn,bruker_id "
        "FROM innlegg i JOIN brukere b ON bruker_id = b.id WHERE i.id = ?",
        (id,)).fetchone()
    return post

def get_all_posts():
    posts = get_db().execute("SELECT i.id,tittel,i.innhold,i.dato_postet,brukernavn,i.bruker_id, "
                             "COUNT(k.id) AS ant_kommentar "
                       "FROM innlegg i JOIN brukere b ON i.bruker_id = b.id "
                       "LEFT JOIN kommentar k on k.innlegg_id = i.id "
                       "GROUP BY i.id "
                       "ORDER BY i.dato_postet DESC "
                       ).fetchall()
    return posts

def add_comment(content,post,user):
    db = get_db()
    db.execute("INSERT INTO kommentar (innhold,innlegg_id,bruker_id) VALUES (?,?,?)",
               (content,post["id"],user["id"]))
    db.commit()
    
def get_comment(id):
    comment = get_db().execute(
        "SELECT k.id, innhold, dato_postet, innlegg_id,bruker_id, brukernavn "
        "FROM kommentar k JOIN brukere b ON bruker_id = b.id WHERE k.id = ?",
        (id,)).fetchone()
    return comment

def get_comments_from_post(id):
    comments = get_db().execute(
        "SELECT k.id, innhold, dato_postet, innlegg_id,bruker_id, brukernavn "
        "FROM kommentar k JOIN brukere b on bruker_id = b.id WHERE innlegg_id = ?",
        (id,)).fetchall()
    return comments