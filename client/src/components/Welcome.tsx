import { Component } from 'react'

interface Props {
    id: number;
}

interface State {
    buttonClicked: boolean;
}

class Welcome extends Component<Props, State> {
    constructor(props: Props) {
        super(props)
        this.state = {
            buttonClicked: false,
        }
    }

    render() {
        if (!this.state.buttonClicked) {
            return (
                <button onClick={() => this.click()}>
                    Click me, id={this.props.id}
                </button>
            )
        } else {
            return (
                <h1>Thanks for clicking, id={this.props.id}</h1>
            )
        }
    }

    click() {
        this.setState({
            buttonClicked: true,
        })
    }
}

export default Welcome
