import { Component } from 'react'

interface Props {
    id: number;
}

interface State {}

class Welcome extends Component<Props, State> {
    render() {
        return <h1>Class Component #{this.props.id}</h1>
    }
}

export default Welcome
