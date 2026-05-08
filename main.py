from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import date
from typing import Literal, Optional

app = FastAPI()

# Banco em memória
pessoas = []

# Modelo da Pessoa
class Pessoa(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    cpf: str = Field(..., pattern=r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$|^\d{11}$')
    data_nascimento: date
    sexo: Literal['M', 'F', 'Outro']

# Modelo para Atualização
class PessoaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    sexo: Optional[Literal['M', 'F', 'Outro']] = None

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
# ATUALIZAR PESSOA
# ============================================================
@app.put('/pessoas/{cpf}')
def atualizar_pessoa(cpf: str, dados_atualizados: PessoaUpdate):
    for pessoa in pessoas:
        if pessoa['cpf'] == cpf:
            # Atualiza apenas os campos que foram enviados
            if dados_atualizados.nome is not None:
                pessoa['nome'] = dados_atualizados.nome
            if dados_atualizados.sexo is not None:
                pessoa['sexo'] = dados_atualizados.sexo
            return {
                'mensagem': 'Pessoa atualizada com sucesso.',
                'dados': pessoa
            }
    
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
