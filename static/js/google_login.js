import {
    auth,
    provider,
    signInWithPopup,
    signOut
} from "./firebase.js";


// ==============================
// Student Google Login
// ==============================

const studentBtn = document.getElementById("googleStudentLogin");

if(studentBtn){

    studentBtn.addEventListener("click", async ()=>{

        try{

            const result = await signInWithPopup(auth, provider);

            const user = result.user;

            const idToken = await user.getIdToken();

            fetch("/student/google-login",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    token:idToken

                })

            })

            .then(res=>res.json())

            .then(data=>{

                if(data.success){

                    window.location=data.redirect;

                }else{

                    alert(data.message);

                }

            });

        }

        catch(error){

            console.error(error);

            alert("Google Login Failed");

        }

    });

}



// ==============================
// Company Google Login
// ==============================

const companyBtn=document.getElementById("googleCompanyLogin");

if(companyBtn){

    companyBtn.addEventListener("click",async()=>{

        try{

            const result=await signInWithPopup(auth,provider);

            const user=result.user;

            const idToken=await user.getIdToken();

            fetch("/company/google-login",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    token:idToken

                })

            })

            .then(res=>res.json())

            .then(data=>{

                if(data.success){

                    window.location=data.redirect;

                }else{

                    alert(data.message);

                }

            });

        }

        catch(error){

            console.error(error);

            alert("Google Login Failed");

        }

    });

}
async function googleLogout() {

    try {

        await signOut(auth);

        window.location.href = "/";

    } catch (error) {

        console.error(error);

    }

}