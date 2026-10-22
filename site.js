
// 希望時間の候補（平日・休日共通、18:00まで）
const TIMES=["09:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00"];
(function initBooking(){
  if(!document.getElementById("bDate")) return;
  const d=new Date(); d.setDate(d.getDate()+2);
  const min=d.toISOString().slice(0,10);
  ["bDate","bDate2","bDate3"].forEach(id=>{ document.getElementById(id).min=min; });
  ["bTime","bTime2","bTime3"].forEach(id=>{
    const sel=document.getElementById(id);
    sel.innerHTML='<option value="">時間を選んでください</option>'+TIMES.map(t=>`<option value="${t}">${t}</option>`).join("");
  });
})();
function onLtChange(){
  const lt=document.querySelector("input[name=lt]:checked")?.value||"";
  document.getElementById("durField").style.display = (lt==="その他のご相談") ? "none" : "block";
}
function fmtDate(v){ if(!v) return ""; return new Date(v+"T00:00:00").toLocaleDateString("ja-JP",{month:"long",day:"numeric",weekday:"short"}); }

function toggleMenu(){
  const l = document.querySelector(".nav-links");
  if(l.style.display==="flex"){
    l.style.display="none";
  } else {
    l.style.cssText="display:flex;flex-direction:column;position:fixed;top:64px;left:0;right:0;background:var(--white);padding:20px 32px;gap:14px;border-bottom:1px solid var(--peach-light);z-index:99;";
  }
}

function toggleFaq(btn){
  btn.closest(".faq-item").classList.toggle("open");
}

async function submitForm(){
  const name=document.getElementById("bName").value.trim();
  const email=document.getElementById("bEmail").value.trim();
  const date=document.getElementById("bDate").value;
  const time=document.getElementById("bTime").value;
  const ltBase=document.querySelector("input[name=lt]:checked")?.value||"";
  const lt = ltBase==="その他のご相談" ? ltBase : ltBase+"（"+document.getElementById("bDur").value+"）";
  const note=document.getElementById("bNote").value;
  const fmt2check = document.getElementById("bFormat").value; if(!name||!email||!date||!time||!fmt2check){ alert("お名前、メールアドレス、希望日、希望時間、レッスン形式は必須です。"); return; }

  const btn = document.querySelector(".form-submit");
  btn.textContent = "送信中...";
  btn.disabled = true;

  try {
    const res = await fetch("https://formspree.io/f/xykbdqvk", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name, email, lessonType: lt,
        format: document.getElementById("bFormat").value,
        "第1希望": fmtDate(date) + " " + time,
        "第2希望": fmtDate(document.getElementById("bDate2").value) + " " + document.getElementById("bTime2").value,
        "第3希望": fmtDate(document.getElementById("bDate3").value) + " " + document.getElementById("bTime3").value,
        message: note
      })
    });

    if (res.ok) {
      const fmt=fmtDate(date);
      document.getElementById("bConfirmBox").innerHTML=`
        <div class="confirm-row"><span class="ck">お名前</span><span class="cv">${name}</span></div>
        <div class="confirm-row"><span class="ck">レッスン</span><span class="cv">${lt}</span></div>
        <div class="confirm-row"><span class="ck">日時</span><span class="cv">${fmt} ${time}</span></div>
        <div class="confirm-row"><span class="ck">メール</span><span class="cv">${email}</span></div>
      `;
      document.getElementById("bForm").style.display="none";
      document.getElementById("bSuccess").style.display="block";
      window.scrollTo({top:document.getElementById("booking").offsetTop-80,behavior:"smooth"});
    } else {
      alert("送信に失敗しました。お手数ですがLINEよりお問い合わせください。"); window.open("https://line.me/R/ti/p/@036bejox","_blank");
      btn.textContent = "予約リクエストを送る 🌸";
      btn.disabled = false;
    }
  } catch(e) {
    alert("送信に失敗しました。お手数ですがLINEよりお問い合わせください。"); window.open("https://line.me/R/ti/p/@036bejox","_blank");
    btn.textContent = "予約リクエストを送る 🌸";
    btn.disabled = false;
  }
}

async function submitBiz(){
  const org=document.getElementById("bzOrg").value.trim(), name=document.getElementById("bzName").value.trim(), email=document.getElementById("bzEmail").value.trim();
  if(!org||!name||!email){ alert("会社名・ご担当者名・メールアドレスは必須です。"); return; }
  const btn=document.querySelector(".biz-submit"); btn.textContent="送信中..."; btn.disabled=true;
  try{
    const res=await fetch("https://formspree.io/f/xykbdqvk",{method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({"種別":"企業向けお問い合わせ",company:org,name,email,message:document.getElementById("bzNote").value})});
    if(res.ok){ document.getElementById("bizForm").style.display="none"; document.getElementById("bizDone").style.display="block"; return; }
  }catch(e){}
  alert("送信に失敗しました。お手数ですが shoko112show@gmail.com までメールでご連絡ください。");
  btn.textContent="お問い合わせを送る"; btn.disabled=false;
}

function resetBooking(){
  ["bName","bEmail","bDate","bDate2","bDate3","bNote","bTime","bTime2","bTime3"].forEach(id=>document.getElementById(id).value="");
  document.getElementById("bForm").style.display="block";
  document.getElementById("bSuccess").style.display="none";
}

document.addEventListener("DOMContentLoaded",()=>{});
const obs=new IntersectionObserver(entries=>{
  entries.forEach(e=>{ if(e.isIntersecting) e.target.classList.add("visible"); });
},{threshold:.1});
document.querySelectorAll(".reveal").forEach(el=>obs.observe(el));
