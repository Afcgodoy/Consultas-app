import streamlit as st
from openai import OpenAI

# Inicialize o cliente OpenAI com sua chave de API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ID do assistente existente (obtido do código anterior)
assistant_id = "asst_ovt3GmLpdpGKG4qGjYTAWshX"  # Substitua pelo ID do assistente criado anteriormente

# Título do app
st.title("Assistente RAG para Consultas de Contribuinte")

# Inicialize o estado da sessão para armazenar a thread e o histórico de mensagens
if "thread_id" not in st.session_state:
   thread = client.beta.threads.create()
   st.session_state.thread_id = thread.id
   st.session_state.messages = []

# Exiba o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
       st.markdown(message["content"])

# Campo de input para a pergunta do usuário
user_input = st.chat_input("Pergunta:")

if user_input:
    # Adicione a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
       st.markdown(user_input)

    # Envie a mensagem para o assistente
    message = client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
       role="user",
       content=user_input
    )

   # Execute o assistente
    run = client.beta.threads.runs.create_and_poll(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant_id
    )

   # Recupere a resposta do assistente
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=st.session_state.thread_id)
        # Pegue a última mensagem do assistente
        for msg in messages:
            if msg.role == "assistant":
                response = msg.content[0].text.value
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)
                break
    else:
        st.error(f"Erro: A execução falhou com status: {run.status}")