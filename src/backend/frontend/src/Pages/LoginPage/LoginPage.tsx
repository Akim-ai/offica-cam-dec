import React, {useRef, useState} from 'react';
import {TextInput} from "../../Components/Inputs";
import {BaseContainer} from "../../Components/Containers";

function LoginPage() {
    const usernameRef = useRef<HTMLInputElement>(null);
    const passwordRef = useRef<HTMLInputElement>(null);
    const [errorMessage, setErrorMessage] = useState<string>();

    const onSubmitLoginForm = (e: React.MouseEvent<HTMLButtonElement>) => {
        if(!usernameRef?.current?.value){
            setErrorMessage(() => 'No username provided');
            return
        }
        else if (!passwordRef?.current?.value) {
            setErrorMessage(() => 'No password provided')
            return
        }
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                'username': usernameRef.current.value,
                'password': passwordRef.current.value
            })
        };
        let user: any = fetch('http://localhost:8000/api/user/auth_token/', requestOptions)
            .then(res => res.json())
        console.log(user)
    }


    return (
        <BaseContainer>
            <div className="
                w-screen h-screen
                flex justify-center items-center
                bg-primary-300
            ">
                <div className="
                    w-1/5 h-1/3
                    p-2.5
                    rounded-md
                    bg-primary-700
                    flex flex-col
                    justify-center items-center
                ">
                    <div>
                    <TextInput inputRef={usernameRef} placeholder={'Username'}/>
                    </div>
                    <div className="mt-2.5"></div>
                    <TextInput inputRef={passwordRef} placeholder={'Password'}/>
                    <button onClick={onSubmitLoginForm}
                        className="mt-5 w-64 h-10 rounded-md boder border-2 border-slate-400 bg-primary-400 text-f_text-100 font-bold ">
                        Login
                    </button>
                    {(errorMessage) ? <div className="mt-2.5 text-amber-500 text-xl font-bold">{errorMessage}</div> : ''}
                </div>
            </div>
        </BaseContainer>
    );
}

export default LoginPage;