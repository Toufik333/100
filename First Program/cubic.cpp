#include <OpenGL/GL/glut.h>
#include <cmath>

struct Point {
    float x, y;
};

Point bezier(float t, Point p0, Point p1, Point p2, Point p3) {
    float u = 1 - t;
    float tt = t * t;
    float uu = u * u;
    float uuu = uu * u;
    float ttt = tt * t;

    Point p;
    p.x = uuu * p0.x + 3 * uu * t * p1.x + 3 * u * tt * p2.x + ttt * p3.x;
    p.y = uuu * p0.y + 3 * uu * t * p1.y + 3 * u * tt * p2.y + ttt * p3.y;
    return p;
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT);
    glBegin(GL_LINE_STRIP);

    Point p0 = {100, 100};
    Point p1 = {150, 300};
    Point p2 = {250, 300};
    Point p3 = {300, 100};

    for (float t = 0; t <= 1.0; t += 0.01) {
        Point p = bezier(t, p0, p1, p2, p3);
        glVertex2f(p.x, p.y);
    }

    glEnd();
    glFlush();
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutCreateWindow("Bezier Curve");
    glutInitWindowSize(400, 400);
    gluOrtho2D(0, 400, 0, 400);
    glutDisplayFunc(display);
    glutMainLoop();
    return 0;
}
