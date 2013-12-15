# coding: utf-8

"""
Main script for nihreporter quepy.
"""
import sys
import logging
import quepy
import time
import datetime
import random
import urllib
import json
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:2020/sparql")
nihreporter = quepy.install("nihreporter")

service_url = 'http://localhost:2020/sparql'

#quepy.set_loglevel("DEBUG")

target, query, metadata = nihreporter.get_query("What is lambert?")

def print_define(results, target, metadata=None):
    for result in results["results"]["bindings"]:
        if result[target]["xml:lang"] == "en":
            print result[target]["value"]
            #print


def print_enum(results, target, metadata=None):
    used_labels = []

    for result in results["results"]["bindings"]:
        if result[target]["type"] == u"literal":
            #if result[target]["xml:lang"] == "en":
            label = result[target]["value"]
            if label not in used_labels:
                used_labels.append(label)
                print label


def print_literal(results, target, metadata=None):
    for result in results["results"]["bindings"]:
        literal = result[target]["value"]
        if metadata:
            print metadata.format(literal)
        else:
            print literal


def print_time(results, target, metadata=None):
    gmt = time.mktime(time.gmtime())
    gmt = datetime.datetime.fromtimestamp(gmt)

    for result in results["results"]["bindings"]:
        offset = result[target]["value"].replace(u"−", u"-")

        if "to" in offset:
            from_offset, to_offset = offset.split("to")
            from_offset, to_offset = int(from_offset), int(to_offset)

            if from_offset > to_offset:
                from_offset, to_offset = to_offset, from_offset

            from_delta = datetime.timedelta(hours=from_offset)
            to_delta = datetime.timedelta(hours=to_offset)

            from_time = gmt + from_delta
            to_time = gmt + to_delta

            location_string = random.choice(["where you are",
                                             "your location"])

            print "Between %s and %s, depending %s" % \
                  (from_time.strftime("%H:%M"),
                   to_time.strftime("%H:%M on %A"),
                   location_string)

        else:
            offset = int(offset)

            delta = datetime.timedelta(hours=offset)
            the_time = gmt + delta

            print the_time.strftime("%H:%M on %A")


def request(query):
    params = {'query': query, 'Content-Type':'application/sparql-results+json', 'output':'json'}
    url = service_url + '?' + urllib.urlencode(params)
    #responses = urllib.urlopen(url).read()
    #print "---"+responses
    responses = json.loads(urllib.urlopen(url).read())
    return responses


def result_from_responses(responses, target):
    if responses:
        to_explore = responses["results"]
        for key in target:
            _to_explore = []
            for elem in to_explore:
                #print elem[0]
                for response in elem:
                    #print response
                    _to_explore.append(response)
            to_explore = _to_explore
            
        print to_explore
        result = []
        for elem in to_explore:
            if isinstance(elem, dict):
                if "lang" in elem:
                    if elem["lang"] == "/lang/en":
                        result.append(elem.get("value", elem))
                else:
                    result.append(elem.get("value", elem))
            else:
                result.append(elem)
        return result



if __name__ == "__main__":
    default_questions = [
        "What is a car?",
        #"Who is Tom Cruise?",
        "Who is George Lucas?",
        "Who is Mirtha Legrand?",
        "List Microsoft software",
        "Name Fiat cars",
        "time in argentina",
        "what time is it in Chile?",
        "List movies directed by Martin Scorsese",
        "How long is Pulp Fiction",
        "which movies did Mel Gibson starred?",
        "When was Gladiator released?",
        "who directed Pocahontas?",
        "actors of Fight Club",
    ]

    if "-d" in sys.argv:
        quepy.set_loglevel("DEBUG")
        sys.argv.remove("-d")

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        questions = [question]
    else:
        questions = default_questions

    print_handlers = {
        "define": print_define,
        "enum": print_enum,
        "time": print_time,
        "literal": print_literal
    }

    for question in questions:
        print question
        print "-" * len(question)

        target, query, metadata = nihreporter.get_query(question)

        if isinstance(metadata, tuple):
            query_type = metadata[0]
            metadata = metadata[1]
        else:
            query_type = metadata
            metadata = None

        if query is None:
            print "Query not generated :(\n"
            continue

        print query
        
        #print target
        
        
        
        #responses = request(query)
        #print responses
        #if "error" in responses:
         #   print responses
          #  exit()
       # else:
         #   for response in result_from_responses(responses, target):
          #      print response
        
        
        
        
        
        
        

        if target.startswith("?"):
            target = target[1:]
        if query:
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            
#            print results
            if not results["results"]["bindings"]:
                print "No answer found :("
                continue
            print_handlers[query_type](results, target, metadata)
#         print
