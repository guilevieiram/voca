import { useState } from "react";
import { BsPencil, BsSave } from "react-icons/bs";

type EditableLineProps = {
    apiKey: string,
    label: string,
    placeholder: string,
    inputType: string,
    changeFunction: (key: string, value: string) => void
};

const validateEmail = (email: string): boolean => {
    return String(email)
        .toLowerCase()
        .match(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/) !== null;
};

export default function EditableLine ({ apiKey, label, placeholder, inputType, changeFunction }: EditableLineProps): React.ReactElement {
    const [enableEdit, setEnableEdit] = useState<boolean>(false);
    const [field, setField] = useState<string>("");
    const onChangeField = (event: any): void => setField(event.target.value);
    const editFunction = (): void => {
        setEnableEdit(true);
    };
    const saveFunction = (event: any): void => {
        event.preventDefault();
        if(inputType === "email" && !validateEmail(field)){
            window.alert("Please input a valid email.");
            return
        }
        setEnableEdit(false);
        changeFunction(apiKey, field);
    };

    return (
        <form className="my-8 w-full">
            <span className="flex w-full justify-between items-center">
                <p className="my-2">{label}</p>
                {
                    enableEdit ? 
                    <button onClick={saveFunction} className="cursor-pointer"><BsSave/></button> :
                    <button onClick={editFunction} className="cursor-pointer"><BsPencil/></button>
                }
            </span>
            <input onChange={onChangeField} className="border border-blue rounded-md bg-transparent w-full px-4 py-1" type={inputType} disabled={!enableEdit} placeholder={placeholder} />
        </form>

    )
};