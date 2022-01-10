import { useState } from 'react';
import {BiDownArrow} from 'react-icons/bi';

export default function Tutorial (): React.ReactElement {
    const [expand, setExpand] = useState<boolean>(false);
    const toggleExpand = (): void => setExpand(!expand)
    return (
        <div className="w-full mt-10">
            <h2 className="py-6 text-2xl">Not sure how to get started?</h2>
            <p onClick={toggleExpand} className='flex flex-row w-full justify-around items-center secondary-button my-6 text-dark dark:text-light '>Check out the tutorial! <span  className={expand ? "transform rotate-180" : ""}><BiDownArrow /></span></p>
            {
                !expand ? <></> :
                <div className="w-full text-justify">
                    <p className='py-2'>After signing up to Voca and logging in (both of which you've already done!) you need to add words to your personal list. You can access that page by the plus sign (+) button in the bottom of the page. There you input all the new vocabulary you want to train, in the language that you want to learn. The best moments to do that is during a class, or when you're reading a text. After, just hit save and all will be recorded in our databases!</p>
                    <p className='py-2'>After you added words in your list you'll be able to play with them! Just go to the play page (in the play-like button in the bottom of the page) and well ... play! It goes like this: for each word that appears you should give your translation (it can be in your mother tongue, in English, or any other language in which you can remember the translation. After that, our Machine Learning algorithm will kick in to determine how close to the answer you were. The words that you know less will appear more often, and the ones you know better will appear less often.</p>
                    <p className="py-2">If you want to see of modify anything in your profile, just go to the home button in the bottom. The same if you want to change any configurations of the app (like switching between light and dark mode), just go to the settings page in the bottom right.</p>
                    <p className='py-2'>And ... thats it! This tutorial will be here if you need it! Good learning!</p>
                </div>
            }
        </div>
    )
};