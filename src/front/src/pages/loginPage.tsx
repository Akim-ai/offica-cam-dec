import {useRef, useState} from "react";


const LoginPage = () => {

    const usernameRef: React.MutableRefObject<HTMLInputElement | null> = useRef(null);
    const passwordRef: React.MutableRefObject<HTMLInputElement | null>  = useRef(null);

    const [credentialsError, setCredentialsError] = useState("");

    async function checkCredentials(){
        console.log(123)
        if(!usernameRef?.current?.value){
            setCredentialsError("No username provided")
            return
        }

        if(!passwordRef?.current?.value){
            setCredentialsError("No password provided")
            return
        }

        const requestOptions = {
            method: 'POST',
            mode: 'no-cors', // Set the request's mode to 'no-cors'
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                "username": usernameRef.current?.value,
                "password": passwordRef.current?.value,
            })
        };
    }

    return (
        <div className='flex flex-col'>
        <input type="text" placeholder="username" ref={usernameRef}/>
        <input type="password" placeholder="password" ref={passwordRef}/>
            <button onClick={checkCredentials}>Submit</button>
            {credentialsError ? credentialsError : ''}
        </div>
    )
}
export {LoginPage}
