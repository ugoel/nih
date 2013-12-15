# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Basic questions for NIH Reporter.
"""

from refo import Group, Plus, Question
from quepy.parsing import Lemma, Pos, QuestionTemplate, Token, Particle, \
                          Lemmas
from quepy.dsl import HasKeyword, IsRelatedTo, HasType
from dsl import DefinitionOf, LabelOf, TitleOf, FiscalYear, FirstName, AppId, ProjAppId, AgencyName, AgencyAppId

# Openings
LISTOPEN = Lemma("list") | Lemma("name")


class Thing(Particle):
    regex = Question(Pos("JJ")) + (Pos("NN") | Pos("NNP") | Pos("NNS")) |\
            Pos("VBN")

    def interpret(self, match):
        return HasKeyword(match.words.tokens)


class WhatIs(QuestionTemplate):
    """
    Regex for questions like "What is a blowtorch
    Ex: "What is a car"
        "What is Seinfield?"
    """

    regex = Lemma("what") + Lemma("be") + Question(Pos("DT")) + \
        Thing() + Question(Pos("."))

#    print "test2"
    
    def interpret(self, match):
        label = DefinitionOf(match.thing)

        return label, "define"


class ListEntity(QuestionTemplate):
    """
    Regex for questions like "List Microsoft software"
    """

    entity = Group(Pos("NNP"), "entity")
    target = Group(Pos("NN") | Pos("NNS"), "target")
    regex = LISTOPEN + entity + target
    
#    print "test1"

    def interpret(self, match):
        entity = FirstName(match.entity.tokens)
        entity = AppId(entity)
        entity = ProjAppId(entity)
        #target_type = HasKeyword(match.target.lemmas)
        #print target_type
        #target =  IsRelatedTo(entity)
        label = TitleOf(entity)
        
        return label, "enum"


class ListProjects(QuestionTemplate):
    """
    Regex for questions like "List Projects 2013"
    """

    entity = Group(Pos("NN") | Pos("NNS"), "entity")
    prep = Group(Pos("IN"), "prep")
    target = Group(Pos("CD"), "target")
    regex = LISTOPEN + entity + prep + target
    
#    print "test"
#    print regex

    def interpret(self, match):
        #entity = HasKeyword(match.entity.tokens)
        #print "--"+match.target.lemmas
        #target_type = HasKeyword(match.target.lemmas)
        year = match.target.lemmas
        target_t = FiscalYear(year)
        #target = HasType(target_type) + IsRelatedTo(entity)
        #target = HasType(target_type)
        #target_t = target_t + "^^<http://www.w3.org/2001/XMLSchema#integer>"
        label = TitleOf(target_t)

        #print "match3"
        
        return label, "enum"


class WhereIsQuestion(QuestionTemplate):
    """
    Ex: "where in the world is the Eiffel Tower" projects funded by national ins cnter
    """

    thing = Group(Plus(Pos("NP") | Pos("NNP") | Pos("NNPS")),
                  "thing")
    entity = Group(Pos("NN") | Pos("NNS"), "entity")
    verb = Group(Plus(Pos("VBD") | Pos("IN")), "verb")
    
    regex = entity + verb + thing

    def interpret(self, match):
        print "checked"
        thing = AgencyName(match.thing.tokens)
        entity = AgencyAppId(thing)
        entity = ProjAppId(entity)
        #target_type = HasKeyword(match.target.lemmas)
        #print target_type
        #target =  IsRelatedTo(entity)
        label = TitleOf(entity)

        return label, "enum"