import { Component } from 'react'

interface Props {
    id: number;
}

interface State {
    showWelcome: boolean;
}

class Welcome extends Component<Props, State> {
    constructor(props: Props) {
        super(props)
        this.state = {
            showWelcome: false,
        }
    }

    render() {
        return (
            <>
                <button onClick={this.click}>
                    Click me, id={this.props.id}
                </button>
                {this.renderWelcome()}
            </>
        )
    }

    renderWelcome(): JSX.Element {
        return this.state.showWelcome ? (
            <h1>Welcome, id={this.props.id}</h1>
        ) : <></>
    }

    click = () => {
        this.setState((state, _props) => ({
            showWelcome: !state.showWelcome,
        }))
    }
}

export default Welcome
