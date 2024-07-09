import "./userCard.css";

import React, {Component} from "react";
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';

const style = {
    py: 0,
    width: '100%',
    maxWidth: 360,
    borderRadius: 2,
    border: '1px solid',
    borderColor: 'divider',
    backgroundColor: 'background.paper',
};

export class UserCard extends Component {
    render() {
        return (
            <List sx={style}>
                <ListItem>
                    <ListItemText primary={this.props.name}/>
                </ListItem>
                <Divider component="li"/>

            </List>

        );
    }
}