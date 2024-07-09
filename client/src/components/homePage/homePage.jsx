import React, {Component} from "react";
import {HomeDiv, HomeTitleContainer, HomeTitleTag,} from "./HomeComponents";
import {Container} from "reactstrap";

export class HomePage extends Component {
    render() {
        return (
            <HomeDiv>
                <HomeTitleContainer>
                    <HomeTitleTag>Status:</HomeTitleTag>
                    <li>{this.props.okStatus}!</li>
                </HomeTitleContainer>
            </HomeDiv>

        );
    }
}
