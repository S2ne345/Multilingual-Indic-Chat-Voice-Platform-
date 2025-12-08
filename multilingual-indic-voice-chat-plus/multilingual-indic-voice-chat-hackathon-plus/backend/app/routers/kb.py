
from fastapi import APIRouter
from app.models.schemas import KBItem
from app.services.rag_vector import VectorKB
router = APIRouter()
kb = VectorKB()
@router.get('/kb')
def list_kb():
    return {'count': len(kb.docs), 'samples': kb.docs[:5]}
@router.post('/kb')
def add_kb(item: KBItem):
    kb.add(item.text, item.source or 'api')
    return {'status': 'ok'}
