export default function ExplanatoryText ():React.ReactElement {
    return (
        <div className="w-full my-10">
            <h2 className="my-6 text-2xl">What is Voca?</h2>
            <div className=" text-justify">
                <p className="my-4">Voca is a language learning app that uses top of the line Machine Learning language processing to provide you with the best learning experience.</p>
                <p className="my-4">Its purpose is to help you learn systematically new vocabulary. So, all those lists of vocabulary that you have in your notebook from when you studied French or Spanish have now a purpose! You will be able to play guessing words to train yourself and achieve mastery in the desired language!</p>
                <p className="my-4">It was developed by a small team of software devs (in this case, only me, Guile) in the start of 2022. So, we are always open to suggestions, help and feedback from our users!</p>
            </div>
            <div className="py-4 text-sm text-gray-400">
                <p className="">All rights reserved ©</p>
                <p className="">Guile Vieira - 2022</p>

            </div>
        </div>
    )
}