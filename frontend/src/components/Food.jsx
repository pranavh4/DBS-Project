import React, { Component } from "react";
import { Button } from "@material-ui/core";

class Food extends Component {
  constructor(props) {
    super(props);
    this.state = { foods: [], name: "", expiry: "", status: "0" };
    this.onSubmit = this.onSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  componentDidMount() {
    fetch("/getFoods")
      .then(res => res.json())
      .then(res => this.setState({ foods: res.food_items }));
  }

  handleChange(event) {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    const name = target.name;
    this.setState({
      [name]: value
    });
  }

  onSubmit() {
    this.setState({ status: "0" });
    fetch("/addFood", {
      method: "POST",
      body: JSON.stringify({
        name: this.state.name,
        expiry: this.state.expiry
      }),
      headers: {
        "Content-Type": "application/json"
      }
    })
      .then(res => res.json())
      .then(res => this.setState({ status: res.status }));
  }

  printStatus() {
    if (this.state.status === "1") {
      return <h2>Succesfully Added Donation</h2>;
    } else if (this.state.status === "-1") {
      return <h2>Unable to Add Donation</h2>;
    }
  }

  render() {
    return (
      <div style={{ textAlign: "center" }}>
        <h1>Current Food Items</h1>
        <table>
          <tr>
            <th className="foodItems">Food ID</th>
            <th className="foodItems">Food Name</th>
            <th className="foodItems">Days Till Expiry</th>
          </tr>
          {this.state.foods.map(food => (
            <tr>
              <td className="foodItems">{food.id}</td>
              <td className="foodItems">{food.name}</td>
              <td className="foodItems">{food.expiry}</td>
            </tr>
          ))}
        </table>
        <h1>Add Food Item</h1>
        Food Name:{" "}
        <input
          type="text"
          name="name"
          value={this.state.name}
          onChange={this.handleChange}
        />
        <br />
        <br />
        Days Till Expiry:{" "}
        <input
          type="text"
          name="expiry"
          value={this.state.expiry}
          onChange={this.handleChange}
        />
        <br />
        <br />
        <Button variant="contained" color="primary" onClick={this.onSubmit}>
          Add Food Item
        </Button>
        <br />
        <br />
        {this.printStatus()}
      </div>
    );
  }
}

export default Food;
