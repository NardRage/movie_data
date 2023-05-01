# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     build_data
   Description :   
   Author :       admin
   date：          2023/4/22
-------------------------------------------------
   Change Activity:
                   2023/4/22 15:11: 
-------------------------------------------------
"""

import json
import os

from py2neo import Graph, Node


class RoleGraph:
    def __init__(self):
        cur_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        self.data_path_film = os.path.join(cur_dir, 'json_data/film.json')
        self.data_path_institution = os.path.join(cur_dir, 'json_data/institution.json')
        self.data_path_shadow_man = os.path.join(cur_dir, 'json_data/shadow-man.json')
        self.g = Graph("bolt://localhost:7687", auth=('neo4j', '202214829dj!'), secure=False)

    '''读取文件'''

    def read_node(self):
        # 共3类主节点
        film = []  # 影视作品
        shadow_man = []  # 影人 [导演、演员]
        institution = []  # 机构

        # 属性节点
        type = []
        country = []
        showing_area = []

        shadow_man_infos = []  # 影人 信息
        film_infos = []  # 影视信息
        institution_infos = []  # 机构信息

        # 构建节点实体关系

        rels_act_in = []  # 参演 演员 --> 影视作品
        rels_make = []  # 制作 导演 --> 影视作品
        rels_work = []  # 工作 影人 [导演、演员] --> 机构
        rels_manufacture = []  # 出品 机构 --> 影视作品

        # 属性节点关系
        rels_type = []
        rels_country = []
        rels_showing_area = []

        count1 = 0
        for data in open(self.data_path_film):
            print(data)
            film_data = {}
            count1 += 1
            print(count1)
            data_json = json.loads(data)
            name_str = data_json['name']
            film.append(name_str)

            film_data['name'] = name_str
            film_data['type'] = ''
            film_data['country'] = ''
            film_data['rating']=''
            film_data['showing_area'] = ''
            film_data['actor'] = ''
            film_data['year'] = ''
            film_data['director'] = ''

            if 'type' in data_json:
                type_str = data_json['type']
                type.append(type_str)
                film_data['type'] = data_json['type']
                rels_type.append([name_str, type_str])

            if 'country' in data_json:
                country_str = data_json['country']
                country.append(country_str)
                film_data['country'] = data_json['country']
                rels_country.append([country_str, name_str])

            if 'showing_area' in data_json:
                showing_area_str = data_json['showing_area']
                showing_area.append(showing_area_str)
                film_data['showing_area'] = data_json['showing_area']
                rels_showing_area.append([name_str, showing_area_str])

            if 'actor' in data_json:
                film_data['actor'] = data_json['actor']
                for actor_str in data_json['actor']:
                    film_data['actor'] = actor_str
                    rels_act_in.append([actor_str, name_str])

            if 'director' in data_json:
                director = data_json['director']
                film_data['director'] = director
                rels_make.append([director, name_str])

            if 'rating' in data_json:
                director = data_json['rating']
                film_data['rating'] = director

            if 'year' in data_json:
                director = data_json['year']
                film_data['year'] = director

            film_infos.append(film_data)

        count2 = 0
        for data in open(self.data_path_institution, encoding='utf-8'):
            institution_dict = {}  # 创建字典
            count2 += 1
            print(count2)
            data_json = json.loads(data)
            name_str = data_json['name']
            institution.append(name_str)
            institution_dict['name'] = name_str
            institution_dict['shadow_man'] = ''
            institution_dict['film_name'] = ''

            if 'shadow_man' in data_json:
                institution_dict['shadow_man'] = data_json['shadow_man']
                for shadow_man_value in data_json['shadow_man']:
                    shadow_man.append(shadow_man_value)
                    rels_work.append([shadow_man_value, name_str])

            if 'film_name' in data_json:
                institution_dict['film_name'] = data_json['film_name']
                for film_value in data_json['film_name']:
                    film.append(film_value)
                    rels_manufacture.append([name_str, film_value])

            institution_infos.append(institution_dict)

        count3 = 0
        for data in open(self.data_path_shadow_man, encoding='utf-8'):
            shadow_man_dict = {}  # 创建字典
            count3 += 1
            print(count3)
            data_json = json.loads(data)
            name_str = data_json['name']
            shadow_man.append(name_str)
            shadow_man_dict['name'] = name_str
            shadow_man_dict['sex'] = ''
            shadow_man_dict['data_of_birth'] = ''
            shadow_man_dict['birth_place'] = ''
            shadow_man_dict['occupation'] = ''

            if 'sex' in data_json:
                shadow_man_dict['sex'] = data_json['sex']

            if 'data_of_birth' in data_json:
                shadow_man_dict['data_of_birth'] = data_json['data_of_birth']

            if 'birth_place' in data_json:
                shadow_man_dict['birth_place'] = data_json['birth_place']

            if 'occupation' in data_json:
                shadow_man_dict['occupation'] = data_json['occupation']

            shadow_man_infos.append(shadow_man_dict)

        print(fr'共读取信息影视作品:{count1}部、影视机构:{count2}、影人:{count3}')

        return set(type), set(country), set(showing_area), set(film), set(shadow_man), set(
            institution), shadow_man_infos, film_infos, institution_infos, rels_act_in, rels_make, rels_work, rels_manufacture, rels_type, rels_country, rels_showing_area

    '''建立节点'''

    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(label, count, len(nodes))
        return

    '''创建知识图谱中心影人实体的节点'''

    def create_shadow_man_nodes(self, shadow_man_infos):
        count = 0
        for disease_dict in shadow_man_infos:
            node = Node("shadow_man", name=disease_dict['name'], sex=disease_dict['sex'],
                        data_of_birth=disease_dict['data_of_birth'], birth_place=disease_dict['birth_place'],
                        occupation=disease_dict['occupation']
                        )
            self.g.create(node)
            count += 1
            print(count)
        return

    def create_film_nodes(self, film_infos):
        count = 0
        for disease_dict in film_infos:
            node = Node("film", name=disease_dict['name'], type=disease_dict['type'],
                        country=disease_dict['country'], showing_area=disease_dict['showing_area'],
                        actor=disease_dict['actor'], director=disease_dict['director']
                        )
            self.g.create(node)
            count += 1
            print(count)
        return

    def create_institution_nodes(self, institution_infos):
        count = 0
        for disease_dict in institution_infos:
            node = Node("institution", name=disease_dict['name'], shadow_man=disease_dict['shadow_man'],
                        film_name=disease_dict['film_name'],
                        )
            self.g.create(node)
            count += 1
            print(count)
        return

    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        for i in range(len(edges)):
            p = str(edges[i][0])
            q = str(edges[i][1])

            query = "match(p:%s),(q:%s) where p.name='%s' and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name
            )
            try:
                self.g.run(query)
                count += 1
                print(query)

            except Exception as e:
                print(e)

    def create_graphrels(self):
        type, country, showing_area, film, shadow_man, institution, shadow_man_infos, film_infos, institution_infos, rels_act_in, rels_make, rels_work, rels_manufacture, rels_type, rels_country, rels_showing_area = self.read_node()
        self.create_relationship('shadow_man', 'film', rels_act_in, 'rels_act_in', '参演  演员 --> 影视作品')
        self.create_relationship('shadow_man', 'film', rels_make, 'rels_make', '制作 导演 --> 影视作品')
        self.create_relationship('shadow_man', 'institution', rels_work, 'rels_work', '工作 影人 [导演、演员] --> 机构')
        self.create_relationship('institution', 'film', rels_manufacture, 'rels_manufacture', '出品 机构 --> 影视作品')
        self.create_relationship('film', 'type', rels_type, 'rels_type', '影视作品 --- 类型')
        self.create_relationship('film', 'country', rels_country, 'rels_country', '语言 --> 影视作品')
        self.create_relationship('film', 'showing_area', rels_showing_area, 'rels_showing_area', '上映地区 --> 影视作品')

    def create_graphnodes(self):
        type, country, showing_area, film, shadow_man, institution, shadow_man_infos, film_infos, institution_infos, rels_act_in, rels_make, rels_work, rels_manufacture, rels_type, rels_country, rels_showing_area = self.read_node()
        self.create_node('type', type)
        self.create_node('country', country)
        self.create_node('showing_area', showing_area)
        self.create_shadow_man_nodes(shadow_man_infos)
        self.create_film_nodes(film_infos)
        self.create_institution_nodes(institution_infos)




from py2neo import Graph
import random

tx = Graph("bolt://localhost:7687", auth=('neo4j', '202214829dj!'), secure=False)


def create_same_level_relations(tx):
    # 查询所有的实体
    query = "MATCH (n:film) RETURN n.name AS name"
    result = tx.run(query)
    entities = [record["name"] for record in result]


    # 对于每个实体，随机选择最多2个其他实体，建立same_level关系
    for entity in entities:
        same_level_count = 0
        while same_level_count < 1:
            other_entity = random.choice(entities)
            if entity != other_entity:
                query = "MATCH (a:film {name: $entity}), (b:film {name: $other_entity}) MERGE (a)-[:same_type]->(b)"
                tx.run(query, entity=entity, other_entity=other_entity)
                same_level_count += 1


create_same_level_relations(tx)


# if __name__ == '__main__':
#     handler = RoleGraph()  # 实例化对象  连接neo4j
#
#     handler.create_graphnodes()  # 创建节点
#     handler.create_graphrels()  # 创建关系
