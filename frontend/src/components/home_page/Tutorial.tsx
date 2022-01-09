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
                    <p className='py-2'>Lorem ipsum dolor sit amet consectetur adipisicing elit. Laboriosam molestiae dicta vitae similique modi deleniti, laborum expedita ratione dolorem dolores odio error alias, blanditiis adipisci ad eaque quam earum necessitatibus.</p>
                    <p className='py-2'>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Repellendus harum beatae ipsum excepturi rerum! Magni nemo porro maxime dolorem deserunt.</p>
                </div>
            }
        </div>
    )
};