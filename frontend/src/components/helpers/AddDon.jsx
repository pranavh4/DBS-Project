import React, { Component } from "react";
import { Button } from "@material-ui/core";

class AddDon extends Component {
  constructor(props) {
    super(props);
    this.state = {
      donor: "",
      dist: "",
      date: "",
      food_id: "",
      quantity: "",
      status: "0"
    };
    this.handleChange = this.handleChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
  }

  printStatus() {
    if (this.state.status === "1") {
      return <h2>Succesfully Added Donation</h2>;
    } else if (this.state.status === "-1") {
      return <h2>Unable to Add Donation</h2>;
    }
  }

  onSubmit() {
    this.setState({ status: "0" });
    fetch("/addDon", {
      method: "POST",
      body: JSON.stringify({
        donor: this.state.donor,
        dist: this.state.dist,
        date: this.state.date,
        food_id: this.state.food_id,
        quantity: this.state.quantity
      }),
      headers: {
        "Content-Type": "application/json"
      }
    })
      .then(res => res.json())
      .then(res => this.setState({ status: res.status }));
  }

  handleChange(event) {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    const name = target.name;
    this.setState({
      [name]: value
    });
  }

  render() {
    return (
      <div style={{ width: "50%", float: "left" }}>
        <h1>Add Donation</h1>
        Enter Donor ID:{" "}
        <input
          type="text"
          name="donor"
          value={this.state.donor}
          onChange={this.handleChange}
        />
        <br />
        <br />
        Enter Distributor ID:{" "}
        <input
          type="text"
          name="dist"
          value={this.state.dist}
          onChange={this.handleChange}
        />
        <br />
        <br />
        Enter Date:{" "}
        <input
          type="text"
          name="date"
          value={this.state.date}
          onChange={this.handleChange}
          placeholder="YYYY-MM-DD"
        />
        <br />
        <br />
        Enter Food ID separated by space:{" "}
        <input
          type="text"
          name="food_id"
          value={this.state.food_id}
          onChange={this.handleChange}
        />
        <br></br>
        <br />
        Enter Respective Quantities:{" "}
        <input
          type="text"
          name="quantity"
          value={this.state.quantity}
          onChange={this.handleChange}
        />
        <br />
        <br />
        <Button variant="contained" color="primary" onClick={this.onSubmit}>
          Add Donation
        </Button>
        <br />
        <br />
        {this.printStatus()}
      </div>
    );
  }
}

export default AddDon;
