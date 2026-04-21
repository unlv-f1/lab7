#!/usr/bin/env python3
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import rclpy
from ackermann_msgs.msg import AckermannDriveStamped
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

# TODO CHECK: include needed ROS msg type headers and libraries


@dataclass  # (Think of Python dataclasses like structs in C/C++)
class Waypoint:
    """Represents a waypoint."""

    x: float
    y: float
    is_key: bool

    @classmethod
    def from_row_dict(cls, d: dict[str, str]) -> Waypoint:
        """Converts from a dictionary mapping names to string representations
        of values."""
        x = float(d["x"])
        y = float(d["y"])
        is_key = convert_str_to_bool(d["is_key"])
        return cls(x=x, y=y, is_key=is_key)


def convert_str_to_bool(s: str) -> bool:
    """Helper function to convert a string to a boolean."""
    if s == "True":
        return True
    elif s == "False":
        return False
    raise ValueError(f"Value must either be 'True' or 'False', got: {s!r}")


def load_waypoints(waypoints_file_path: Path) -> list[Waypoint]:
    """Loads waypoints from a file."""

    waypoints: list[Waypoint] = []
    with open(str(waypoints_file_path)) as f:
        reader = csv.DictReader(f)
        for row_dict in reader:
            waypoints.append(Waypoint.from_row_dict(row_dict))
    return waypoints


class PurePursuit(Node):
    """Runs Pure Pursuit."""

    def __init__(self):
        super().__init__("pure_pursuit_node")

        # TODO: Create ROS subscribers and publishers, initialize attributes,
        #       load waypoints

        self.get_logger().info(f"{self.get_name()} initialized.")

    def scan_callback(self, scan_msg: LaserScan) -> None:
        pass
        # TODO: Consider using scan data somehwere?

    def odom_callback(self, odom_msg: Odometry) -> None:
        pass
        # TODO: Find the current waypoint to track using methods mentioned in lecture
        # TODO: Transform goal point to vehicle frame of reference
        # TODO: Calculate steering angle
        # TODO: Publish drive message


def main(args=None):
    """Main entry point function."""
    rclpy.init(args=args)
    node = PurePursuit()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
