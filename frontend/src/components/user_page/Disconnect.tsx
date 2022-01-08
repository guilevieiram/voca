export default function Disconnect (): React.ReactElement {
    const disconnect = (): void => {
        sessionStorage.clear();
        window.location.reload();
    };
    return <button onClick={disconnect} className="secondary-button border-red text-red w-full my-10">Disconnect.</button>
};