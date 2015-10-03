from middleware import db


class Configuration(db.Model):
    """
    Mapping the database structure
    """
    __tablename__ = 'configuration'
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50), unique=True)
    host = db.Column(db.String(255))
    token = db.Column(db.String(50))

    def __repr__(self):
        return '<Configuration %r>' % self.team_name
