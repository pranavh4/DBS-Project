from surplusfood import db

class DONATING_ORG(db.Model):
    Donor_id = db.Column(db.Integer, primary_key=True)
    D_Org_name = db.Column(db.String(30), nullable=False)
    Address = db.Column(db.String(120), nullable=False)
    Phone = db.Column(db.String(13), unique=True)
    Email = db.Column(db.String(25), unique=True)

    def __init__(self, Donor_id, D_Org_name, Address, Phone, Email):
        self.Donor_id = Donor_id
        self.D_Org_name = D_Org_name
        self.Address = Address
        self.Phone = Phone
        self.Email = Email


class RECEIVING_ORG(db.Model):
    Receiver_id = db.Column(db.Integer, primary_key=True)
    R_Org_name = db.Column(db.String(30), nullable=False)
    Address = db.Column(db.String(120), nullable=False)
    Phone = db.Column(db.String(13), unique=True)
    Email = db.Column(db.String(25), unique=True)

    def __init__(self, Receiver_id, R_Org_name, Address, Phone, Email):
        self.Receiver_id = Receiver_id
        self.R_Org_name = R_Org_name
        self.Address = Address
        self.Phone = Phone
        self.Email = Email


class DISTRIBUTOR(db.Model):
    Dist_id = db.Column(db.Integer, primary_key=True)
    Dist_name = db.Column(db.String(30), nullable=False)
    Address = db.Column(db.String(120), nullable=False)
    Phone = db.Column(db.String(13), unique=True)
    Email = db.Column(db.String(25), unique=True)

    def __init__(self, Dist_id, Dist_name, Address, Phone, Email):
        self.Dist_id = Dist_id
        self.Dist_name = Dist_name
        self.Address = Address
        self.Phone = Phone
        self.Email = Email


class DONATION(db.Model):
    Donation_id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date())
    Donor_id = db.Column(db.Integer, db.ForeignKey("DONATING_ORG.Donor_id"))
    Dist_id = db.Column(db.Integer, db.ForeignKey("DISTRIBUTOR.Dist_id"))

    def __init__(self, Date, Donation_id, Donor_id, Dist_id):
        self.Donation_id = Donation_id
        self.Date = Date
        self.Donor_id = Donor_id
        self.Dist_id = Dist_id


class RECEIPT(db.Model):
    Receipt_id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date())
    Receiver_id = db.Column(db.Integer, db.ForeignKey("RECEIVING_ORG.Receiver_id"))
    Dist_id = db.Column(db.Integer, db.ForeignKey("DISTRIBUTOR.Dist_id"))

    def __init__(self, Receipt_id, Date, Receiver_id, Dist_id):
        self.Receipt_id = Receipt_id
        self.Date = Date
        self.Receiver_id = Receiver_id
        self.Dist_id = Dist_id


class FOOD_ITEM(db.Model):
    Food_id = db.Column(db.Integer, primary_key=True, nullable=False)
    Food_name = db.Column(db.String(30), nullable=False)
    Days_till_expiry = db.Column(db.Integer)

    def __init__(self, Food_id, Food_name, Days_till_expiry):
        self.Food_id = Food_id
        self.Food_name = Food_name
        self.Days_till_expiry = Days_till_expiry


class DONATION_CONTAINS(db.Model):
    Donation_id = db.Column(db.Integer, db.ForeignKey("DONATION.Donation_id"), primary_key=True)
    Food_id = db.Column(db.Integer, db.ForeignKey("FOOD_ITEM.Food_id"), primary_key=True)
    Amount = db.Column(db.Integer)

    def __init__(self, Donation_id, Food_id, Amount):
        self.Donation_id = Donation_id
        self.Food_id = Food_id
        self.Amount = Amount


class RECEIPT_CONTAINS(db.Model):
    Receipt_id = db.Column(db.Integer, db.ForeignKey("RECEIPT.Receipt_id"), primary_key=True)
    Food_id = db.Column(db.Integer, db.ForeignKey("FOOD_ITEM.Food_id"), primary_key=True)
    Amount = db.Column(db.Integer)

    def __init__(self, Receipt_id, Food_id, Amount):
        self.Receipt_id = Receipt_id
        self.Food_id = Food_id
        self.Amount = Amount