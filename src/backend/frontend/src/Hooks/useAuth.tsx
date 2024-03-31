import { useEffect } from 'react';
import {useNavigate} from "react-router-dom";

const useAuth = () => {
    const navigate = useNavigate()

    useEffect(() => {
        // Your authentication logic goes here
        const isAuthenticated = /* Check if the user is authenticated */ false;

        if (!isAuthenticated) {
            navigate('login/');
        }
    }, );

    return {
    };
};

export default useAuth;
