/**
 * @source https://github.com/kirstenlindsmith/PoseNet_React/blob/master/client/components/utils.js
 */

import * as posenet from '@tensorflow-models/posenet';

function toTuple({x, y}) {
    return [x, y]
}

function drawSegment(
    [firstX, firstY],
    [nextX, nextY],
    color,
    lineWidth,
    scale,
    canvasContext
) {
    canvasContext.beginPath()
    canvasContext.moveTo(firstX * scale, firstY * scale)
    canvasContext.lineTo(nextX * scale, nextY * scale)
    canvasContext.lineWidth = lineWidth
    canvasContext.strokeStyle = color
    canvasContext.stroke()
}

export function drawSkeleton(keypoints, minConfidence, canvasContext) {
    const adjacentKeyPoints = posenet.getAdjacentKeyPoints(
        keypoints,
        minConfidence
    )

    adjacentKeyPoints.forEach(keypoints => {
        drawSegment(
            toTuple(keypoints[0].position),
            toTuple(keypoints[1].position),
            'blue',
            6,
            1,
            canvasContext
        )
    })
}
