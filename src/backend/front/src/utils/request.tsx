interface IRequest{
    method: string;
    url: string;
    body?: string;
}

export const request = async (props: IRequest) => {
    let requestOptions;
    if (props?.body){
        
        requestOptions = {
            method: props.method,
            headers: { 'Content-Type': 'application/json' },
            body: props.body
        };
    }
    else{
        requestOptions = {
            method: props.method,
            headers: { 'Content-Type': 'application/json' },
        };
    }


    return fetch(`http://127.0.0.1:8000/api/${props.url}`, requestOptions)
    .then( res => res.json() );
}
