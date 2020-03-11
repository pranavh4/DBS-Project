import React, { Component } from "react";
import "../tempo.css";
import { width } from "@material-ui/system";

class Alert extends Component {
  constructor(props) {
    super(props);
    this.state = {
      color: this.props.type === "danger" ? "red" : "green"
    };
  }
  render() {
    return (
      // <div className="register" style={this.props.style}>
      <p
        style={{
          borderColor: this.state.color,
          width: "25%",
          display: "inline-block",
          marginTop: "1%"
        }}
        className={"alert alert-" + this.props.type}
        role="alert"
      >
        {this.props.message}
      </p>
      // </div>
    );
  }
}

export default Alert;
