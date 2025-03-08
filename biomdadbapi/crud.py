# -*- encoding: utf-8 -*-
# @File: crud.py

from sqlmodel import Session, select, and_, or_
from .models import (Compound2cid, Cid2ssimcid, Disease2doid, Doid2gene,
                    Protein2stringid, PPIv12, Pnodev12, ExptCPI, ExptPnode,
                    CPIv5, CCIv5, PPIv10p5, Pnodev10p5, Cnodev5)
from .utilities import string2md5, row_to_dict
from .database import engine
import re

async def sel_compound2cid(compound: list[str]):
    md5sum = [string2md5(x.strip()) for x in compound]
    md5sum2compound = [{'md5sum': x, 'compound': y}
               for x, y in zip(md5sum, compound)]
    with Session(engine) as session:
        stmt = select(Compound2cid).where(Compound2cid.md5sum.in_(md5sum))
        md5sum2cid = session.exec(stmt).all()
    if (len(md5sum2cid) == 0):
        res = None
    else:
        md5sum2cid = row_to_dict(Compound2cid, md5sum2cid)
        res = {'md5sum2cid': md5sum2cid, 'md5sum2compound': md5sum2compound}
    return res

async def sel_cid2ssimcid(cid: list[str]):
    with Session(engine) as session:
        stmt = select(Cid2ssimcid).where(Cid2ssimcid.cid.in_(cid))
        cid2ssimcid = session.exec(stmt).all()
    if (len(cid2ssimcid) == 0):
        res = None
    else:
        cid2ssimcid = row_to_dict(Cid2ssimcid, cid2ssimcid)
        res = {'cid2ssimcid': cid2ssimcid}
    return res

async def sel_disease2doid(disease: str, fixed: bool):
    if re.match(r'^DOID:[0-9]+$', disease):
        with Session(engine) as session:
            stmt = (select(Disease2doid).
                    where(Disease2doid.doid == disease))
            d2doid = session.exec(stmt).all()
    else:
        if fixed:
            with Session(engine) as session:
                stmt = (select(Disease2doid).
                        where(Disease2doid.disease == disease))
                d2doid = session.exec(stmt).all()
        else:
            patt = f'%{disease}%'
            with Session(engine) as session:
                stmt = (select(Disease2doid).
                        where(Disease2doid.disease.like(patt)))
                d2doid = session.exec(stmt).all()
    if (len(d2doid) == 0):
        res = None
    else:
        d2doid = row_to_dict(Disease2doid, d2doid)
        res = {'d2doid': d2doid}
    return res

async def sel_doid2gene(doid: str):
    with Session(engine) as session:
        stmt = select(Doid2gene).where(Doid2gene.doid == doid)
        doid2gene = session.exec(stmt).all()
    if (len(doid2gene) == 0):
        res = None
    else:
        doid2gene = row_to_dict(Doid2gene, doid2gene)
        res = {'doid2gene': doid2gene}
    return res

async def sel_protein2stringid(protein: list[str]):
    with Session(engine) as session:
        stmt = (select(Protein2stringid).
                where(Protein2stringid.protein.in_(protein)))
        p2string = session.exec(stmt).all()
    if (len(p2string) == 0):
        res = None
    else:
        p2string = row_to_dict(Protein2stringid, p2string)
        res = {'p2string': p2string}
    return res

async def sel_string_ppi(stringid: list[str], score: int):
    with Session(engine) as session:
        stmt1 = (select(PPIv12).
                where(and_(or_(PPIv12.node1.in_(stringid),
                               PPIv12.node2.in_(stringid)),
                           PPIv12.score >= score)))
        edges1 = session.exec(stmt1).all()
    if (len(edges1) == 0):
        res = None
    else:
        edges1 = row_to_dict(PPIv12, edges1)
        spid1 = [row['node1'] for row in edges1]
        spid2 = [row['node2'] for row in edges1]
        all_spid = list(set(spid1 + spid2))
        new_spid = [sid for sid in all_spid if sid not in stringid]
        if (len(new_spid) < 2):
            edges = edges1
        else:
            with Session(engine) as session:
                stmt2 = (select(PPIv12).
                         where(and_(PPIv12.node1.in_(new_spid),
                                    PPIv12.node2.in_(new_spid),
                                    PPIv12.score >= score)))
                edges2 = session.exec(stmt2).all()
            edges2 = row_to_dict(PPIv12, edges2)
            edges = edges1 + edges2
        with Session(engine) as session:
            stmt3 = (select(Pnodev12).
                     where(Pnodev12.stringv12.in_(all_spid)))
            nodes = session.exec(stmt3).all()
        nodes = row_to_dict(Pnodev12, nodes)
        res = {'edges': edges, 'nodes': nodes}
    return res

async def sel_expt_cpi(stitchid: list[str], score: int):
    with Session(engine) as session:
        stmt1 = (select(ExptCPI).
                 where(and_(ExptCPI.node1.in_(stitchid),
                            ExptCPI.experiment >= score)))
        ecpi = session.exec(stmt1).all()
    if (len(ecpi) == 0):
        res = None
    else:
        ecpi = row_to_dict(ExptCPI, ecpi)
        stringid = [row['node2'] for row in ecpi]
        with Session(engine) as session:
            stmt2 = select(ExptPnode).where(ExptPnode.stringv10p5.in_(stringid))
            epnode = session.exec(stmt2).all()
        epnode = row_to_dict(ExptPnode, epnode)
        res = {'ecpi': ecpi, 'epnode': epnode}
    return res


async def sel_stitch_cpi(stitchid: list[str], score: int):
    with Session(engine) as session:
        stmt1 = (select(CPIv5).
                 where(and_(or_(CPIv5.node1.in_(stitchid),
                                CPIv5.node2.in_(stitchid)),
                            CPIv5.score >= score)))
        cpi = session.exec(stmt1).all()
    if (len(cpi) == 0):
        res = None
    else:
        cpi = row_to_dict(CPIv5, cpi)
        scid = [row['node1'] for row in cpi]
        scid = list(set(scid))
        spid = [row['node2'] for row in cpi]
        spid = list(set(spid))
        if (len(scid) < 2):
            cci = None
        else:
            with Session(engine) as session:
                stmt2 = (select(CCIv5).
                        where(and_(CCIv5.node1.in_(scid),
                                   CCIv5.node2.in_(scid),
                                   CCIv5.score >= score)))
                cci = session.exec(stmt2).all()
            cci = row_to_dict(CCIv5, cci)
        if (len(spid) < 2):
            ppi = None
        else:
            with Session(engine) as session:
                stmt3 = (select(PPIv10p5).
                        where(and_(PPIv10p5.node1.in_(spid),
                                   PPIv10p5.node2.in_(spid),
                                   PPIv10p5.score >= score)))
                ppi = session.exec(stmt3).all()
            ppi = row_to_dict(PPIv10p5, ppi)
        edges = {'cpi': cpi, 'cci': cci, 'ppi': ppi}

        with Session(engine) as session:
            stmt4 = select(Cnodev5).where(Cnodev5.stitchv5.in_(scid))
            cnodes = session.exec(stmt4).all()
        with Session(engine) as session:
            stmt5 = select(Pnodev10p5).where(Pnodev10p5.stringv10p5.in_(spid))
            pnodes = session.exec(stmt5).all()
        nodes = {'cnodes': cnodes, 'pnodes': pnodes}
        res = {'edges': edges, 'nodes': nodes}
    return res