function togglePassword(){

    const password=document.getElementById("password");

    const eye=document.getElementById("eye");

    if(password.type==="password"){

        password.type="text";

        eye.classList.remove("fa-eye");

        eye.classList.add("fa-eye-slash");

    }

    else{

        password.type="password";

        eye.classList.remove("fa-eye-slash");

        eye.classList.add("fa-eye");

    }

}
// const glow=document.querySelector(".mouse-glow");

// // document.addEventListener("mousemove",(e)=>{

// //     if(glow){

// //         glow.style.left=e.clientX+"px";

// //         glow.style.top=e.clientY+"px";

// //     }

// // });
const form=document.querySelector("form");

const button=document.querySelector(".login-btn");

if(form){

form.addEventListener("submit",()=>{

button.disabled=true;

button.innerHTML=`

<i class="fa-solid fa-spinner fa-spin"></i>

Logging In...

`;

});

}
const counters=document.querySelectorAll(".stat-box h2");

counters.forEach(counter=>{

const update=()=>{

const target=parseInt(counter.innerText);

const count=parseInt(counter.getAttribute("data-count"))||0;

const speed=25;

if(count<target){
const value=count+Math.ceil(target/speed);
counter.setAttribute("data-count",value);
counter.innerText=value+"+";
requestAnimationFrame(update);
}
else{
counter.innerText=target+"+";
}
};
update()
});
// const card=document.querySelector(".login-card");

// if(card){

// card.addEventListener("mousemove",(e)=>{

// const rect=card.getBoundingClientRect();

// const x=e.clientX-rect.left;

// const y=e.clientY-rect.top;

// const rotateX=-(y-rect.height/2)/18;

// const rotateY=(x-rect.width/2)/18;

// card.style.transform=`

// perspective(1200px)

// rotateX(${rotateX}deg)

// rotateY(${rotateY}deg)

// scale(1.02)

// `;

// });

// card.addEventListener("mouseleave",()=>{

// card.style.transform="perspective(1200px) rotateX(0) rotateY(0) scale(1)";

// });