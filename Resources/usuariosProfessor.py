from datetime import datetime
from flask import jsonify, make_response, abort

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")  # Local
# client = MongoClient('localhost', 27017)
db = client.clientes


def get_dict_from_mongodb():
    itens_db = db.clientes.find()
    PEOPLE = {}
    for i in itens_db:
        print("teste i before")
        print(i)
        i.pop('_id')  # retira id: criado automaticamente
        item = dict(i)
        print("teste item sem I")
        print(item)
        print("teste item lname")
        print(item["lname"])
        print("teste i after REMOVE")
        print(i)
        # Changing to use the lastName as ID
        PEOPLE[item["lname"]] = (i)
        print("PEOOPLE")
        print(PEOPLE)
    return PEOPLE


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_all():
    PEOPLE = get_dict_from_mongodb()
    dict_clientes = [PEOPLE[key] for key in sorted(PEOPLE.keys())]
    print(" list of items:")
    print(dict_clientes)
    clientes = jsonify(dict_clientes)
    qtd = len(dict_clientes)
    content_range = "clientes 0-" + str(qtd) + "/" + str(qtd)
    # Configura headers
    clientes.headers['Access-Control-Allow-Origin'] = '*'
    clientes.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    clientes.headers['Content-Range'] = content_range
    return clientes


def read_one(lname):
    PEOPLE = get_dict_from_mongodb()
    if lname in PEOPLE:
        person = PEOPLE.get(lname)
    else:
        abort(
            404, "Pessoa com sobrenome {lname} nao encontrada".format(
                lname=lname)
        )
    return person


def create(person):
    lname = person.get("lname", None)
    fname = person.get("fname", None)
    PEOPLE = get_dict_from_mongodb()
    if lname not in PEOPLE and lname is not None:
        item = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp(),
        }
        db.clientes.insert_one(item)
        return make_response(
            "{lname} criado com sucesso".format(lname=lname), 201
        )
    else:
        abort(
            406,
            "Pessoa com sobrenome {lname} ja existe".format(lname=lname),
        )


def update(lname, person):
    query = {"lname": lname}
    update = {"$set": {
        "lname": lname,
        "fname": person.get("fname"),
        "timestamp": get_timestamp(), }
    }
    PEOPLE = get_dict_from_mongodb()

    if lname in PEOPLE:
        db.clientes.update_one(query, update)
        PEOPLE = get_dict_from_mongodb()
        return PEOPLE[lname]
    else:
        abort(
            404, "Pessoa com sobrenome {lname} nao encontrada".format(
                lname=lname)
        )


def delete(lname):
    query = {"lname": lname}
    PEOPLE = get_dict_from_mongodb()
    if lname in PEOPLE:
        db.clientes.delete_one(query)
        return make_response(
            "{lname} deletado com sucesso".format(lname=lname), 200
        )
    else:
        abort(
            404, "Pessoa com sobrenome {lname} nao encontrada".format(
                lname=lname)
        )
