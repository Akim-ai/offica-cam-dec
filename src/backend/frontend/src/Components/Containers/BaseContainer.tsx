import React from 'react';

interface IBaseContainer{
    children: React.ReactNode[] | React.ReactElement[] | React.ReactElement | React.ReactNode
}

function BaseContainer(props: IBaseContainer) {
    return (
        <div className="w-screen min-h-screen">
            {props.children}
        </div>
    );
}

export default BaseContainer;