type EditableImageProps= {
    apiKey: string,
    placeholder: string,
    changeFunction: (key: string, value: string) => void
};

export default function EditableImage ({ apiKey, placeholder, changeFunction }: EditableImageProps): React.ReactElement {
    return (
        <div className="w-full flex justify-center items-end">
            <div className="h-32 w-32 rounded-full overflow-hidden flex justify-center items-center bg-light border border-blue">
                <img src={placeholder} alt={apiKey} className="object-cover min-h-full min-w-full "/>
            </div>
        </div>
    )
};