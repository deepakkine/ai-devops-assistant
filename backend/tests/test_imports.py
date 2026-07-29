def test_import_chat_service():
    from app.services.chat_service import ChatService

    assert ChatService is not None


def test_import_retriever():
    from app.rag.retriever import Retriever

    assert Retriever is not None