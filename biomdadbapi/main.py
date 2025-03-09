# -*- encoding: utf-8 -*-
# @File: main.py

import uvicorn
from fastapi import FastAPI, HTTPException, Form
from . import crud
from .config import get_config

app = FastAPI()

@app.post('/c2cid/')
async def biomdadb_compound2cid(md5sum: list[str]=Form()):
    res = await crud.sel_compound2cid(md5sum=md5sum)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/cid2ssimcid/')
async def biomdadb_cid2ssimcid(cid: list[str]=Form()):
    res = await crud.sel_cid2ssimcid(cid=cid)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/disease2doid/')
async def biomdadb_disease2doid(disease: str=Form(), fixed: bool=Form()):
    res = await crud.sel_disease2doid(disease=disease, fixed=fixed)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/doid2gene/')
async def biomdadb_doid2gene(doid: str=Form()):
    res = await crud.sel_doid2gene(doid=doid)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/protein2stringid/')
async def biomdadb_protein2stringid(protein: list[str]=Form()):
    res = await crud.sel_protein2stringid(protein=protein)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/stringppi/v12/')
async def biomdadb_string_ppi(stringid: list[str]=Form(), score: int=Form()):
    res = await crud.sel_string_ppi(stringid=stringid, score=score)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/exptcpi/v5/')
async def biomdadb_expt_cpi(stitchid: list[str]=Form(), score: int=Form()):
    res = await crud.sel_expt_cpi(stitchid=stitchid, score=score)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

@app.post('/stitchcpi/v5/')
async def biomdadb_stitch_cpi(stitchid: list[str]=Form(), score: int=Form()):
    res = await crud.sel_stitch_cpi(stitchid=stitchid, score=score)
    if (res is None):
        raise HTTPException(status_code=404)
    else:
        return res

def main():
    conf_opt = get_config()
    host = conf_opt.get('host')
    port = conf_opt.get('port')
    port = int(port)
    uvicorn.run(app='biomdadbapi.main:app', host=host, port=port)