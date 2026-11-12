// Change this if your Flask backend uses another host or port.
const API_BASE = "http://127.0.0.1:5000";
const UPLOAD_ENDPOINT = "/api/documents/upload";
const DOCUMENTS_ENDPOINT = "/api/documents/";
const ASK_ENDPOINT = "/api/chat/ask";

const $ = id => document.getElementById(id);
let documents = [], selectedDocumentId = null;

$("chooseFileBtn").onclick = () => $("fileInput").click();
$("fileInput").onchange = e => { if (e.target.files[0]) uploadDocument(e.target.files[0]); };
["dragenter","dragover"].forEach(name => $("dropZone").addEventListener(name,e=>{e.preventDefault();$("dropZone").classList.add("dragover");}));
["dragleave","drop"].forEach(name => $("dropZone").addEventListener(name,e=>{e.preventDefault();$("dropZone").classList.remove("dragover");}));
$("dropZone").addEventListener("drop",e=>{if(e.dataTransfer.files[0])uploadDocument(e.dataTransfer.files[0]);});
$("refreshDocsBtn").onclick = loadDocuments;
$("newChatBtn").onclick = newConversation;
document.querySelectorAll(".suggestion").forEach(b=>b.onclick=()=>{$("questionInput").value=b.dataset.question;$("chatForm").requestSubmit();});

function toast(message){$("toast").textContent=message;$("toast").classList.add("show");setTimeout(()=>$("toast").classList.remove("show"),2800);}
function showChat(){$("welcomePanel").classList.add("hidden");$("chatArea").classList.remove("hidden");}
function newConversation(){selectedDocumentId=null;$("scopeLabel").textContent="All documents";$("messages").innerHTML='<div class="assistant-message"><div class="avatar">C</div><div><b>CompanyDocs AI</b><p>Ask a question across your indexed company documents.</p></div></div>';$("welcomePanel").classList.remove("hidden");$("chatArea").classList.add("hidden");$("questionInput").value="";renderDocuments();}

async function uploadDocument(file){
 if(!file.name.toLowerCase().endsWith(".pdf"))return toast("Please select a PDF file.");
 const form=new FormData();form.append("file",file);
 $("uploadProgress").classList.add("show");$("progressBar").style.width="20%";$("uploadStatus").textContent="Uploading and indexing PDF...";$("chooseFileBtn").disabled=true;
 try{
  const res=await fetch(API_BASE+UPLOAD_ENDPOINT,{method:"POST",body:form});const data=await res.json();
  if(!res.ok)throw new Error(data.error||data.message||"Upload failed.");
  $("progressBar").style.width="100%";$("uploadStatus").textContent=`Indexed ${data.total_chunks??""} chunks`;
  await loadDocuments();if(data.file_id)selectDocument(data.file_id);toast(`${data.filename||file.name} uploaded successfully.`);
 }catch(err){$("uploadStatus").textContent=err.message;toast(err.message);}
 finally{$("chooseFileBtn").disabled=false;$("fileInput").value="";setTimeout(()=>$("uploadProgress").classList.remove("show"),2200);}
}
async function loadDocuments(){
 try{const res=await fetch(API_BASE+DOCUMENTS_ENDPOINT);const data=await res.json();if(!res.ok)throw new Error(data.error||"Could not load documents.");documents=data.documents||[];renderDocuments();}
 catch(err){$("documentList").innerHTML='<p class="muted">Could not connect to the backend.</p>';console.error(err);}
}
function renderDocuments(){
 $("documentCount").textContent=`${documents.length} document${documents.length===1?"":"s"} indexed`;
 $("documentList").innerHTML="";
 if(!documents.length){$("documentList").innerHTML='<p class="muted">No documents indexed yet.</p>';return;}
 documents.forEach(doc=>{
  const row=document.createElement("div");row.className="doc-item"+(selectedDocumentId===doc.document_id?" active":"");
  const icon=document.createElement("span");icon.className="pdf";icon.textContent="PDF";
  const info=document.createElement("div");info.className="doc-info";
  const title=document.createElement("b");title.textContent=doc.filename;title.title=doc.filename;
  const detail=document.createElement("small");detail.textContent=`${doc.total_chunks} text chunks`;info.append(title,detail);
  const del=document.createElement("button");del.className="delete";del.textContent="×";del.title="Delete indexed document";del.onclick=e=>{e.stopPropagation();removeDocument(doc.document_id,doc.filename);};
  row.append(icon,info,del);row.onclick=()=>selectDocument(doc.document_id);$("documentList").append(row);
 });
}
function selectDocument(id){selectedDocumentId=id;const doc=documents.find(d=>d.document_id===id);$("scopeLabel").textContent=doc?doc.filename:"Selected document";renderDocuments();showChat();$("questionInput").focus();}
async function removeDocument(id,name){
 if(!confirm(`Remove "${name}" from the indexed knowledge base?`))return;
 try{const res=await fetch(API_BASE+DOCUMENTS_ENDPOINT+encodeURIComponent(id),{method:"DELETE"});const data=await res.json();if(!res.ok)throw new Error(data.error||"Delete failed.");if(selectedDocumentId===id)newConversation();await loadDocuments();toast("Document removed from the index.");}
 catch(err){toast(err.message);}
}
$("chatForm").addEventListener("submit",async e=>{
 e.preventDefault();const question=$("questionInput").value.trim();if(!question)return;
 showChat();addMessage("user",question);$("questionInput").value="";$("sendBtn").disabled=true;
 const typing=addTyping();
 try{
  const res=await fetch(API_BASE+ASK_ENDPOINT,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question,file_id:selectedDocumentId})});
  const data=await res.json();if(!res.ok)throw new Error(data.error||data.message||"Could not get an answer.");
  typing.remove();addMessage("assistant",data.answer||"No answer was returned.",data.sources||[]);
 }catch(err){typing.remove();addMessage("assistant",`I couldn't complete that request. ${err.message}`);}
 finally{$("sendBtn").disabled=false;$("questionInput").focus();}
});
function addMessage(role,text,sources=[]){
 const row=document.createElement("div");row.className=role==="user"?"user-message":"assistant-message";
 if(role==="assistant"){const avatar=document.createElement("div");avatar.className="avatar";avatar.textContent="C";row.append(avatar);}
 const body=document.createElement("div");if(role==="assistant"){const author=document.createElement("b");author.textContent="CompanyDocs AI";body.append(author);}
 const p=document.createElement("p");p.textContent=text;body.append(p);
 if(role==="assistant"&&sources.length){const box=document.createElement("div");box.className="sources";const label=document.createElement("div");label.className="sources-title";label.textContent="SOURCES";box.append(label);
  sources.forEach(s=>{const chip=document.createElement("span");chip.className="source-chip";const b=document.createElement("b");b.textContent="PDF";chip.append(b,document.createTextNode(` ${s.filename||"Document"} · Page ${s.page??"?"}`));box.append(chip);});body.append(box);}
 row.append(body);$("messages").append(row);$("messages").scrollTop=$("messages").scrollHeight;
}
function addTyping(){const row=document.createElement("div");row.className="assistant-message typing";row.innerHTML='<div class="avatar">C</div><div>Searching documents and preparing an answer...</div>';$("messages").append(row);return row;}
$("questionInput").addEventListener("input",()=>{const el=$("questionInput");el.style.height="auto";el.style.height=Math.min(el.scrollHeight,120)+"px";});
$("questionInput").addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();$("chatForm").requestSubmit();}});
loadDocuments();