# -*- encoding: utf-8 -*-
# @File: models.py

from sqlmodel import SQLModel, Field, PrimaryKeyConstraint

class Compound2cid(SQLModel, table=True):
    __tablename__ = "compound2cid"
    md5sum: str = Field(primary_key=True)
    cid: str

class Cid2ssimcid(SQLModel, table=True):
    __tablename__ = "cid2ssimcid"
    cid: str = Field(primary_key=True)
    ssimcid: str

class Protein2stringid(SQLModel, table=True):
    __tablename__ = "stringv12protein2stringid"
    __table_args__ = (PrimaryKeyConstraint('protein', 'stringv12'),)
    protein: str = Field()
    stringv12: str

class Disease2doid(SQLModel, table=True):
    __tablename__ = "disease2doid"
    doid: str = Field(primary_key=True)
    disease: str
    superclass: str
    ngene: int

class Doid2gene(SQLModel, table=True):
    __tablename__ = "disease2gene"
    doid: str = Field(primary_key=True)
    entrezid: str

class PPIv12(SQLModel, table=True):
    __tablename__ = "stringv12ppi"
    __table_args__ = (PrimaryKeyConstraint('node1', 'node2'),)
    node1: str
    node2: str
    experiment: int
    fusion: int
    neighborhood: int
    cooccurence: int
    coexpression: int
    database: int
    textmining: int
    score: int
    evidence: str

class Pnodev12(SQLModel, table=True):
    __tablename__ = "stringv12proteininfo"
    stringv12: str = Field(primary_key=True)
    name: str
    entrezid: str
    description: str


class ExptCPI(SQLModel, table=True):
    __tablename__ = "experimentcpi"
    __table_args__ = (PrimaryKeyConstraint('node1', 'node2'),)
    node1: str
    node2: str
    experiment: int

class ExptPnode(SQLModel, table=True):
    __tablename__ = "ecpiproteininfo"
    __table_args__ = (PrimaryKeyConstraint('stringv10p5', 'name'),)
    stringv10p5: str
    name: str
    stringv12: str
    entrezid: str
    description: str

class CPIv5(SQLModel, table=True):
    __tablename__ = "stitchv5cpi"
    __table_args__ = (PrimaryKeyConstraint('node1', 'node2'),)
    node1: str
    node2: str
    experiment: int
    prediction: int
    database: int
    textmining: int
    score: int
    evidence: str

class CCIv5(SQLModel, table=True):
    __tablename__ = "stitchv5cci"
    __table_args__ = (PrimaryKeyConstraint('node1', 'node2'),)
    node1: str
    node2: str
    experiment: int
    database: int
    textmining: int
    score: int
    evidence: str

class PPIv10p5(SQLModel, table=True):
    __tablename__ = "stringv10p5ppi"
    __table_args__ = (PrimaryKeyConstraint('node1', 'node2'),)
    node1: str
    node2: str
    experiment: int
    fusion: int
    neighborhood: int
    cooccurence: int
    coexpression: int
    database: int
    textmining: int
    score: int
    evidence: str

class Pnodev10p5(SQLModel, table=True):
    __tablename__ = "stringv10p5proteininfo"
    stringv10p5: str = Field(primary_key=True)
    name: str
    entrezid: str
    description: str

class Cnodev5(SQLModel, table=True):
    __tablename__ = "stitchv5compoundinfo"
    stitchv5: str = Field(primary_key=True)
    name: str
    pubchemcid: str
    description: str