import bottle
import bottle_pgsql

app = bottle.Bottle()
plugin = bottle_pgsql.Plugin('dbname=db user=user password=pass')
app.install(plugin)

@app.route('/show/:<item>')
def show(item, db):
    db.execute('SELECT * from items where name="%s"', (item,))
    row = db.fetchone()
    if row:
        return template('showitem', page=row)
    return HTTPError(404, "Page not found")