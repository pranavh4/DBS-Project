import React, { Component } from "react";
import AddDon from "./helpers/AddDon";
import AddRec from "./helpers/AddRec";
import "./tempo.css";

class Add extends Component {
  constructor(props) {
    super(props);
    this.state = {
      foods: []
    };
  }

  componentDidMount() {
    fetch("/getFoods")
      .then(res => res.json())
      .then(res => this.setState({ foods: res.food_items }));
  }
  render() {
    return (
      <div style={{ textAlign: "center" }}>
        <h1>Food Items you can Donate</h1>
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
        <AddDon />
        <AddRec />
      </div>
    );
  }
}

export default Add;
