import React, { Component } from "react";
import "./tempo.css";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import { Link } from "react-router-dom";
// import { Redirect } from "react-router-dom";
import Alert from "./helpers/Alert";

class OrgReg extends Component {
  constructor(props) {
    super(props);
    this.state = {
      name: "",
      phone: "",
      email: "",
      address: "",
      success: 0
    };
    this.handleChange = this.handleChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
  }

  alert_printer() {
    if (this.state.success === -1) {
      return (
        <Alert
          type="danger"
          message="Registration Failed"
          style={{ width: "50%", margin: "auto" }}
        />
      );
    } else if (this.state.success === 1) {
      return (
        <Alert
          type="success"
          message="Registration Succesful"
          style={{ width: "50%", marginLeft: "27%" }}
        />
      );
    }
  }

  handleChange(event) {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    const name = target.name;
    this.setState({
      [name]: value
    });
  }

  onSubmit(e) {
    e.preventDefault();
    fetch("/AddOrg", {
      method: "POST",
      body: JSON.stringify({
        name: this.state.name,
        phone: this.state.phone,
        address: this.state.address,
        email: this.state.email,
        type: this.props.type
      }),
      headers: {
        "Content-Type": "application/json"
      }
    })
      .then(res => res.json())
      .then(res => this.setState({ success: res.status }));
  }

  render() {
    return (
      <div className="background">
        <div className="register">
          <label className="spacing" htmlFor="name">
            Enter Organization Name
          </label>
          <br />
          <TextField
            type="Text"
            name="name"
            value={this.state.name}
            onChange={this.handleChange}
          />
          <br />
          <label className="spacing" htmlFor="email">
            Enter Email ID
          </label>
          <br />
          <TextField
            type="Email"
            name="email"
            value={this.state.email}
            onChange={this.handleChange}
          />
          <br />
          <label className="spacing" htmlFor="phone">
            Enter Phone
          </label>
          <br />
          <TextField
            type="text"
            name="phone"
            value={this.state.phone}
            onChange={this.handleChange}
          />
          <br />
          <label className="spacing" htmlFor="address">
            Enter Address
          </label>
          <br />
          <TextField
            type="address"
            name="address"
            value={this.state.address}
            onChange={this.handleChange}
          />
          <br />
          <div className="spacing">
            <Button variant="contained" color="primary" onClick={this.onSubmit}>
              Register
            </Button>
          </div>
        </div>
        {this.alert_printer()}
      </div>
    );
  }
}

export default OrgReg;
