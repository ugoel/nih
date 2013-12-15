# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Domain specific language for DBpedia quepy.
"""

from quepy.dsl import FixedType, HasKeyword, FixedRelation, FixedDataRelation

# Setup the Keywords for this application
HasKeyword.relation = "rdfs:label"
HasKeyword.language = "en"


class IsPerson(FixedType):
    fixedtype = "foaf:Person"


class DefinitionOf(FixedRelation):
    relation = "rdfs:comment"
    reverse = True


class LabelOf(FixedRelation):
    relation = "rdfs:label"
    reverse = True


class TitleOf(FixedRelation):
    relation = "vocab:project_projecttitle"
    reverse = True


class FiscalYear(FixedDataRelation):
    relation = "vocab:project_fiscalyear"
    #language = "en"


class NameOf(FixedRelation):
    relation = "foaf:name"
    # relation = "dbpprop:name"
    reverse = True

class FirstName(FixedDataRelation):
    relation = "vocab:principalinvestigator_pifirstname"

class AppId(FixedRelation):
    relation = "vocab:principalinvestigator_applicationid"
    reverse = True
    
class ProjAppId(FixedRelation):
    relation = "vocab:project_applicationid"
    reverse = False
    
class AgencyName(FixedDataRelation):
    relation = "vocab:agency_icname"
    
class AgencyAppId(FixedRelation):
    relation = "vocab:agency_applicationid"
    reverse = True    