import React, {MutableRefObject} from "react";
interface ITextInput{
    onChange?: (e: React.ChangeEvent<HTMLInputElement>) => {}
    inputRef: MutableRefObject<HTMLInputElement | null>
    placeholder: string
}

function TextInput(props: ITextInput) {
    return (
        <div className="
            w-72 h-10
            rounded-md
            flex items-center justify-center
            bg-primary-400
        ">
            <input ref={props.inputRef} placeholder={props.placeholder} className="
                w-5/6 h-10
                rounded-md
                bg-primary-400
                text-f_text-100
                placeholder:text-f_text-600
                active:outline-none focus:outline-none
                active:border-none
            "/>
        </div>
    );
}

export default TextInput;