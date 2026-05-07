from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date

app = FastAPI()

# Banco em memória
pessoas = []

# Modelo da Pessoa
class Pessoa(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    sexo: str

# ============================================================
# CADASTRAR PESSOA
# ============================================================
@app.post('/pessoas')
def cadastrar_pessoa(pessoa: Pessoa):
    # Verificar CPF duplicado
    for p in pessoas:
        if p['cpf'] == pessoa.cpf:
            raise HTTPException(
                status_code=400,
                detail='CPF já cadastrado.'
            )
    pessoas.append(pessoa.dict())
    return {
        'mensagem': 'Pessoa cadastrada com sucesso.',
        'dados': pessoa
    }

# ============================================================
# LISTAR PESSOAS
# ============================================================
@app.get('/pessoas')
def listar_pessoas():
    return pessoas

# ============================================================
# BUSCAR POR CPF
# ============================================================
@app.get('/pessoas/{cpf}')
def buscar_pessoa(cpf: str):
    for pessoa in pessoas:
        if pessoa['cpf'] == cpf:
            return pessoa
    raise HTTPException(
        status_code=404,
        detail='Pessoa não encontrada.'
    )

# ============================================================
# REMOVER PESSOA
# ============================================================
@app.delete('/pessoas/{cpf}')
def remover_pessoa(cpf: str):
    for pessoa in pessoas:
        if pessoa['cpf'] == cpf:
            pessoas.remove(pessoa)
            return {
                'mensagem': 'Pessoa removida com sucesso.'
            }
    raise HTTPException(
        status_code=404,
        detail='Pessoa não encontrada.'
    )
