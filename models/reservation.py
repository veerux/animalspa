from extensions import db
reservation_list = []


def get_last_id():
    if reservation_list:
        last_reservation = reservation_list[-1]
    else:
        return 1
    return last_reservation.id + 1


class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pet = db.Column(db.String(100))
    service = db.Column(db.String(100))
    is_publish = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
