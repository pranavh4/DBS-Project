from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import traceback
import sys
from datetime import date, timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://newuser:password@localhost/FOOD"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


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

@app.route("/AddOrg", methods=['POST'])
def AddOrg():
    req = request.get_json()
    if "" in req.values():
        return {"status":-1}

    if req['type'] == 'Distributor':
        last_index = DISTRIBUTOR.query.all()
        if last_index:
            last_index = last_index[-1].Dist_id+1
        else:
            last_index=1
        org = DISTRIBUTOR(last_index,req['name'],req['address'],req['phone'],req['email'])
        try:
            db.session.add(org)
            db.session.commit()
            return {"status":1}
        except:
            db.session.rollback()
            return {"status":-1}

    elif req['type'] == 'Donor':
        last_index = DONATING_ORG.query.all()
        if last_index:
            last_index = last_index[-1].Donor_id+1
        else:
            last_index=1
        org = DONATING_ORG(last_index,req['name'],req['address'],req['phone'],req['email'])
        try:
            db.session.add(org)
            db.session.commit()
            return {"status":1}
        except:
            return {"status":-1}

    elif req['type'] == 'Reciever':
        last_index = RECEIVING_ORG.query.all()
        if last_index:
            last_index = last_index[-1].Receiver_id+1
        else:
            last_index=1
        org = RECEIVING_ORG(last_index,req['name'],req['address'],req['phone'],req['email'])
        try:
            db.session.add(org)
            db.session.commit()
            return {"status":1}
        except:
            return {"status":-1}


@app.route("/getDon", methods=['POST'])
def getDon():
    req = request.get_json()
    res={'donations':[]}
    if req['donor']=='':
        if req['dist']=='':
            res['donations'] = DONATION.query.all()
        else:
            res['donations'] = DONATION.query.filter_by(Dist_id=req['dist']).all()
    else:
        if req['dist']=='':
            res['donations'] = DONATION.query.filter_by(Donor_id=req['donor']).all()
        else:
            res['donations'] = DONATION.query.filter_by(Dist_id=req['dist'],Donor_id=req['donor']).all()
    for i in range(len(res['donations'])):
        print(DONATION_CONTAINS.Donation_id)
        foods = DONATION_CONTAINS.query.filter_by(Donation_id = res['donations'][i].Donation_id).all()
        print(foods[0].Food_id)
        for j in range(len(foods)):
            food_name = FOOD_ITEM.query.filter_by(Food_id=foods[j].Food_id).first().Food_name
            foods[j] = {'name':food_name,'quantity':foods[j].Amount}
        res['donations'][i] = {'id': res['donations'][i].Donation_id,'donor':res['donations'][i].Donor_id,'dist':res['donations'][i].Dist_id,'foods':foods}
    return res

@app.route("/getReciept", methods=['POST'])
def getReciept():
    req = request.get_json()
    res={'reciepts':[]}
    if req['reciever']=='':
        if req['dist']=='':
            res['reciepts'] = RECEIPT.query.all()
        else:
            res['reciepts'] = RECEIPT.query.filter_by(Dist_id=req['dist']).all()
    else:
        if req['dist']=='':
            res['reciepts'] = RECEIPT.query.filter_by(Receiver_id=req['reciever']).all()
        else:
            res['reciepts'] = RECEIPT.query.filter_by(Dist_id=req['dist'],Receiver_id=req['reciever']).all()
    for i in range(len(res['reciepts'])):
        foods = RECEIPT_CONTAINS.query.filter_by(Receipt_id = res['reciepts'][i].Receipt_id).all()
        for j in range(len(foods)):
            food_name = FOOD_ITEM.query.filter_by(Food_id=foods[j].Food_id).first().Food_name
            foods[j] = {'name':food_name,'quantity':foods[j].Amount}
        res['reciepts'][i] = {'id': res['reciepts'][i].Receipt_id,'reciever':res['reciepts'][i].Receiver_id,'dist':res['reciepts'][i].Dist_id,'foods':foods}
    return res
            
@app.route("/getFoods")
def getFood():
    foods = FOOD_ITEM.query.all()
    for i in range(len(foods)):
        foods[i] = {"id":foods[i].Food_id,"name":foods[i].Food_name,"expiry":foods[i].Days_till_expiry}
    foods = {"food_items":foods}
    print(foods)
    return foods

@app.route("/addDon",methods=['POST'])
def addDon():
    req = request.get_json()
    last_index = DONATION.query.all()
    if last_index:
        last_index = last_index[-1].Donation_id + 1
    else:
        last_index = 1
    try:
        don = DONATION(req['date'],last_index,req['donor'],req['dist'])
        food_id = req['food_id'].split(' ')
        quantity = req['quantity'].split(' ') 
        db.session.add(don)
        db.session.commit()
        for i in range(len(food_id)):
            don_c = DONATION_CONTAINS(don.Donation_id,food_id[i],quantity[i])
            db.session.add(don_c)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.delete(don)
        db.session.commit()
        traceback.print_exc(file=sys.stdout)
        return {"status":"-1"}
    return {"status":"1"}

@app.route("/addRec",methods=['POST'])
def addRec():
    req = request.get_json()
    last_index = RECEIPT.query.all()
    if last_index:
        last_index = last_index[-1].Receipt_id + 1
    else:
        last_index = 1
    try:
        rec = RECEIPT(last_index,req['date'],req['reciever'],req['dist'])
        food_id = req['food_id'].split(' ')
        quantity = req['quantity'].split(' ') 
        db.session.add(rec)
        db.session.commit()
        don = DONATION.query.filter_by(Dist_id=req['dist']).all()
        don = [x.Dist_id for x in don]
        rec = RECEIPT.query.filter_by(Receipt_id=req['dist']).all()
        rec = [x.Dist_id for x in don]

        for i in range(len(food_id)):
            food = DONATION_CONTAINS.query.filter(DONATION_CONTAINS.Donation_id.in_(don))
            food = food.filter_by(Food_id = food_id[i]).all()
            expiry = FOOD_ITEM.query.get(food_id[i]).Days_till_expiry
            amt_avail = 0
            for j in food:
                don_date = DONATION.query.get(j.Donation_id).Date
                if don_date + timedelta(days=expiry) > date(int(req['date'][:4]),int(req['date'][5:7]),int(req['date'][8:10])):
                    amt_avail += int(j.Amount)
            if amt_avail < int(quantity[i]):
                raise Exception("Insufficient food")
            rec_c = RECEIPT_CONTAINS(rec.Receipt_id,food_id[i],quantity[i])
            db.session.add(rec_c)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.delete(rec)
        db.session.commit()
        traceback.print_exc(file=sys.stdout)
        return {"status":"-1"}
    return {"status":"1"}


# db.create_all(bind='__all__', app=None)
app.run(debug=True)
