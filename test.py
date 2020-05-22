from Model.mongo_conexion import ConexionMongo
from bson import ObjectId
import bson

mg = ConexionMongo("local", "local", "usuarios")
mg.create_conexion("local")


# res = mg.get_dict_from_mongodb(db_inst="local", collection="usuarios")
# print(res)


res_nome = mg.find_one_document(db_inst="local", collection="usuarios",
                                nome="Jorgito")

print("TESTS")
print("res_nome")
print(res_nome)
print(res_nome["_id"]) # bson.objectid.ObjectId
print(type(res_nome["_id"])) #<class 'bson.objectid.ObjectId

print("OBJECTS")
if bson.objectid.ObjectId.is_valid(res_nome["_id"]):
    print ("YES")
else:
    print ("NOPE")

if bson.objectid.ObjectId.is_valid('54f0e5aa313f5d824680d6c9'):
    print ("YES")
else:
    print ("NOPE")

if ObjectId.is_valid("5bb3314919802578051ccf86"):
    print ("True")
else:
    print ("False")

#
# print("INVALIDO")
# res_invalido = mg.find_document(
#     db_inst="local", collection="usuarios", _id="5ec58b01814de331a3c35579")
# print("res_invalido")
# print(res_invalido) # None
# print(type(res_invalido))

