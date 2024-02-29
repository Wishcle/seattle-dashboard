import { FC } from 'react'

interface GreetProps {
    name: string;
}

const Greet:FC<GreetProps> = (props) => {
    return <h1>Hello, {props.name}</h1>
}

export default Greet
