document.addEventListener
("DOMContentLoaded",
    ()=>
        {document.querySelectorAll
            (".delete-form").
            forEach
            (f=>f.addEventListener("submit",e=>{if(!confirm("Delete this story permanently?"))
                e.preventDefault()}));
                setTimeout(()=>document.querySelectorAll(".message").
                forEach(x=>x.remove()),4000);});