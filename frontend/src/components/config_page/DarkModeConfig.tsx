import React from 'react';

enum ThemeOptions {
    dark,
    light,
    systemDefault
};

function updateTheme(theme: ThemeOptions): void {
    console.log('updating theme to ', theme)
    console.log(theme.valueOf() == ThemeOptions.dark.valueOf());
    if(theme.valueOf() == ThemeOptions.dark.valueOf()) localStorage.theme = 'dark';
    else if(theme.valueOf() == ThemeOptions.light.valueOf()) localStorage.theme = 'light';
    else localStorage.removeItem('theme');
    window.location.reload();
};

function getDefaultValue(): ThemeOptions {
    if (localStorage.theme === 'dark') return ThemeOptions.dark;
    else if (localStorage.theme === 'light') return ThemeOptions.light;
    else return ThemeOptions.systemDefault;
};

export default function DarkModeConfig (): React.ReactElement {
    const change = (event: any): void => updateTheme(event.target.value);
    return(
        <div className="flex justify-between items-center my-4 text-dark dark:text-light">
            <p className="">Theme:</p>
            <form action="">
                <select name="" id="" defaultValue={getDefaultValue()} onChange={change} className='text-sm bg-light dark:bg-dark'>
                    <option value={ThemeOptions.dark}>Dark</option>
                    <option value={ThemeOptions.light}>Light</option>
                    <option value={ThemeOptions.systemDefault}>System default</option>
                </select>
            </form>
        </div>
    )
};