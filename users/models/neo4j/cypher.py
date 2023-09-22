from users.connectors.neo4j import drive
from flask import Flask, request, jsonify


class CypherModel:

    def __init__(self):
        pass
    
    def get_users_applications_from_neo4j(self):
        records = drive.execute_query(
        "MATCH (u:USER) -[h:HAS_ACCESS_TO]-> (a:APPLICATION) RETURN u.name, a.name, u.neo_id AS userId",
        database_="neo4j",
        )
        counter = 0
        neo4j_lst = []
        for node in records[0]:
            my_dict = {}
            name = node['u.name']
            application = node['a.name']
            userId = node['userId']
            my_dict['name'] = name
            my_dict['application'] = application
            my_dict['neo_id'] = userId
            neo4j_lst.insert(counter, my_dict)
            counter+=1
        return neo4j_lst
    
    def user_details_by_id(self, id):
        records = drive.execute_query(
        f"MATCH (u:USER) -[h:HAS_ACCESS_TO]-> (a:APPLICATION) WHERE u.neo_id={id} RETURN u, a",
        database_="neo4j",
        )
        if not records[0]:
            return None
        else:
            neo4j_lst = []
            app_list = []
            for node in records[0]:
                my_dict = {}
                node1 = node['u']
                user = node1['name']
                node2 = node['a']
                application = node2['name']
                my_dict['name'] = user
                app_list.append(application)
                my_dict['application'] = app_list
                my_dict['neo_id'] = id
                neo4j_lst.append(my_dict)
            return neo4j_lst[0]
    
    def add_user_application(self, id, user_name, application):
        try:
            for app in application:
                drive.execute_query(
                "MERGE (n:USER{neo_id:%s, name:'%s'}) WITH n MATCH (a:APPLICATION{name:'%s'}) MERGE (n) -[h:HAS_ACCESS_TO]-> (a) RETURN n, a"%(id, user_name, app),
                database_="neo4j",
                )
            return application
        except Exception as e:
            print(e)

    def update_user_applications_by_id(self, id, application):
        try:
            drive.execute_query(
            "MATCH (u:USER)-[r:HAS_ACCESS_TO]->() WHERE u.neo_id=%s DELETE r WITH u MATCH (a:APPLICATION) WHERE a.name IN %s MERGE (u)-[:HAS_ACCESS_TO]->(a)"%(id, application),
            database_="neo4j",
            )
            return application
        except Exception as e:
            print(e)
            
    def delete_user_application(self, id):
        try:
            drive.execute_query(
            "MATCH (n) WHERE n.neo_id=%s DETACH DELETE n"%(id),
            database_="neo4j",
            )
        except Exception as e:
            print(e)
